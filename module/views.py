from datetime import datetime, date
from django.db.models import Q, Sum
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status

from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator, IsLearner
from .models import *
from users.models import CourseEnrollment, ProgramEnrollment, UserProfile
from .serializers import *
from decimal import Decimal
from rest_framework.parsers import MultiPartParser, FormParser
from quiz.models import Grade
from application.serializers import ApplicationSerialzer

# Create your views here.
class MarkComplete(APIView):
    """
    Given the module, course and program name and learner username(string "None" if not part of program),
    mark the module as completed 
    and update overal progress on the program or course.
    """
    permission_classes = [IsLearner, IsContentCreator]

    def calculate_score(self, course, learner):
        #calculate course score b
        course_modules = Module.objects.filter(course=course)
        course_score = Decimal(0)
        num_modules = Decimal(0)
        for module_inst in course_modules:
            module_score = Grade.objects.filter(learner=learner, module=module_inst).aggregate(total=Sum('grade'))
            course_score += module_score['total']
            print("TYEPE OF COURSE_SCORE",type(course_score))
            print("TYEPE OF module_score total",type(module_score["total"]))
            num_modules += Decimal(1)
        return course_score / num_modules if num_modules > 0 else 0

    def update_progress(self,learner, module, course_enrollment, program_enrollments=None):
        
        date = datetime.now()
        course_enrollment.number_of_modules_completed += Decimal(1)
        module_course = course_enrollment.course
        num_modules = module_course.number_of_modules
        completed_modules = course_enrollment.number_of_modules_completed

        cur_progress_course = course_enrollment.progress #current progress in course
        if course_enrollment.progress != 100:
            #update course progress
            progress = (completed_modules / num_modules) * 100
            course_enrollment.progress = progress
            cur_progress_course = course_enrollment.progress 
            course_enrollment.save()

        #check if course is part of any program and update program progress if course is co7mpleted
        if program_enrollments and (cur_progress_course == 100):

            #update each program that conatians the course and  learner is enrolled in
            for program_enrollment in program_enrollments:    
                program_enrollment.number_of_courses_completed += Decimal(1)
                module_program = program_enrollment.program
                num_courses = module_program.number_of_courses
                completed_courses = program_enrollment.number_of_courses_completed

                if program_enrollment.progress != 100:
                    progress = (completed_courses / num_courses) * 100
                    program_enrollment.progress = progress
                    cur_progress_program = program_enrollment.progress #current progress in program
                    program_enrollment.save()
                    #
                    if cur_progress_program == 100:
                        #learner has completed the program after finishing current course 
                        #calculate program score
                        program_courses = module_program.courses.all()
                        prog_score = Decimal(0)
                        count_course = Decimal(0)
                        for course_inst in program_courses:
                           #calculate course score
                            course_score = self.calculate_score(course_inst, learner)#Decimal(0) 
                            prog_score += course_score
                            count_course += Decimal(1)
                        
                        prog_score = prog_score / count_course 
                        formated_score = format(prog_score, '.2f')    
                        LearnerCompletion.objects.get_or_create(learner=learner, 
                                                         module=module, 
                                                         course=module_course,
                                                         program=module_program, 
                                                         score=formated_score, 
                                                         completed_at=date)
                        
                        program_enrollment.status = 'completed'
                        program_enrollment.save()
                        return Response({"message":"program completed successfully!",
                                         "score": prog_score},
                                         status=status.HTTP_200_OK)
                    else:
                        continue

            #learner has completed the course
            
            course_score = self.calculate_score(module_course, learner) #calculate course score
            
            # create it if it does not exist                            
            LearnerCompletion.objects.get_or_create(learner=learner, 
                                             module=module, 
                                             course=module_course, 
                                             completed_at=date, 
                                             score=course_score)
            course_enrollment.status = 'completed'
            course_enrollment.save()
            
            return Response({"message":"course completed successfully!",
                            "score":format(course_score, '.2f')},
                            status=status.HTTP_200_OK)
            
        elif cur_progress_course != 100:
            #learner has completed the module
            result = Grade.objects.get(module=module, learner=learner)
            score = result.grade
            
            LearnerCompletion.objects.get_or_create(learner=learner,
                                              module=module, 
                                              score=score, 
                                              completed_at=date)
            
            return Response({"message":"module completed successfully!",
                             "score":score},
                             status=status.HTTP_200_OK)

        else:
            #learner has completed the course
            course_score = self.calculate_score(module_course, learner)
            LearnerCompletion.objects.get_or_create(learner=learner, 
                                             module=module, 
                                             course=module_course, 
                                             completed_at=date, 
                                             score=course_score)
            course_enrollment.status = 'complete'
            course_enrollment.save()
            
            return Response({"message":"course completed successfully.",
                             "score": course_score},
                             status=status.HTTP_200_OK)

    def patch(self, request, module_id, learner_id):
        
        user = self.request.user
        # get instances
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error":"learner not found"},
                            status=status.HTTP_404_NOT_FOUND)
        
        learner_profile = UserProfile.objects.get(user=learner)
        
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"error":"module does not exist"},
                            status=status.HTTP_404_NOT_FOUND)
        #proceed if module not already completed

        try:
            LearnerCompletion.objects.get(module=module, learner=learner)
        except (LearnerCompletion.DoesNotExist):
            pass
        except LearnerCompletion.MultipleObjectsReturned:
            return Response({"error":"Module already completed"},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error":"Module already completed"},
                            status=status.HTTP_403_FORBIDDEN)
            

        try:
            module_course = Course.objects.get(id=module.course.id) #course where the module belongs to
        except Module.DoesNotExist:
            return Response({"error":"module's course does not exist"},
                            status=status.HTTP_404_NOT_FOUND) 
        
        #check if enrolled in the course
        try:
            course_enrollment = CourseEnrollment.objects.get(Q(learner=learner_profile) & Q(course=module_course))
            is_enrolled_course = True          
        except CourseEnrollment.DoesNotExist:
            is_enrolled_course = False
        else:
            #check deadline
            date_today = date.today()
            deadline = course_enrollment.deadline
            within_deadline = True
            if deadline:
                within_deadline = (deadline >= date_today)

        #check learner has passed all quizs in module then update progress
        num_quizs = module.num_quizs
        quizs_passed = 0
        passed_all_quizs = None
        if num_quizs > 0: 
            quizs_passed = Grade.objects.filter(learner=learner, module=module, passed=True).count()
            
            if num_quizs == quizs_passed:
                passed_all_quizs = True
               
            else:
                passed_all_quizs= False
                return Response({"message":"can not mark module as complete. You have not passed all quizs."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            passed_all_quizs = True
            #create a full score for module ensuring a module is always scored
            Grade.objects.get_or_create(learner=learner, module=module, grade=100, passed=True)

        #if learner is within deadline and is enrolled or user is owner of module update
        if (learner_profile.creator == False) or (user == module.owner):
            if is_enrolled_course and within_deadline and passed_all_quizs:
                
                #course could be part of multiple programs
                module_programs = Program.objects.filter(courses__name=module_course.name)    
                if not module_programs:
                    #course not part of any program
                    update = self.update_progress(learner, module, course_enrollment)
                    return update
                
                #course part of muliple programs
                enrollment_list = []
                for program in module_programs:
                    
                    try:
                        program_enrollment = ProgramEnrollment.objects.get(learner=learner_profile, program=program)
                    except ProgramEnrollment.DoesNotExist:
                        #learner not enrolled in program the course belongs to.
                        continue

                    enrollment_list.append(program_enrollment)

                #if course is part of a program and learner is enrolled in it,  update program progress
                if enrollment_list:  
                    update = self.update_progress(learner, module, course_enrollment, program_enrollments=enrollment_list)
                    return update
            
            else:
                if not is_enrolled_course:
                    return Response({"error":"you do not have permisssion to perform this action. Not enrolled."},
                                    status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"error":"you can not perform this action. Deadline has passed."},
                                    status=status.HTTP_403_FORBIDDEN)
        else:
                return Response({"error":"you do not have permisssion to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)

class AddMedia(APIView):
    """
    Given a module name and a path to a file, add media to a module if module exists
    and request is from owner.
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsContentCreator]

    def post(self, request):

        serializer = AddMediaSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data["media"]
            module_name = serializer.validated_data["module_name"]
            description = serializer.validated_data["description"]
            user = request.user
            try:
                module = Module.objects.get(name=module_name)
            except Module.DoesNotExist:
                return Response({"message":"Can not add media to module. Module does not exist."},
                                 status=status.HTTP_404_NOT_FOUND)
        
            #create media instance if user owns the module
            if user == module.owner:
                Media.objects.create(owner=user, file=file, description=description, module=module)
                return Response({"message":"Added media to module successfully."},
                                status=status.HTTP_200_OK)
            else: 
                return Response({"error":"Can not add media to module. You do not have permission."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            e = serializer.errors
            return Response({"message":"Invalid serializer.",
                             "error":e},
                             status=status.HTTP_400_BAD_REQUEST)
def isEnrolledOrOwner(module, request, obj):
        """
        A helper function to determine whether a user 
        is enrolled in a program or a course the module belongs to.
        """

        is_part_prog = None
        module = module
        module_owner = module.owner
        modules_course = module.course

        #check if course blongs to a program
        try:
            #course might be part of multiple programs
            course_programs = Program.objects.filter(courses=modules_course)
            is_part_prog = True
        except Program.DoesNotExist:
            is_part_prog = False

        requester = request.user
        user_profile = UserProfile.objects.get(user=requester)
        
        #check users enrollment in course
        try:
            CourseEnrollment.objects.get(Q(course=modules_course) & Q(learner=user_profile))
            is_enrolled_course = True
        except CourseEnrollment.DoesNotExist:
            is_enrolled_course = False

        #check if user is enrolled to any program that conatains the course
        is_enrolled_program = None
        if is_part_prog:
            # if user enrolled into atleast one program that conatins the module's course break and assign user as enrolled.
            for program in course_programs:
                try:
                    prog_enrollment = ProgramEnrollment.objects.get(Q(program=program) & Q(learner=user_profile))

                except ProgramEnrollment.DoesNotExist:
                    is_enrolled_program = False
                    continue
                
                else:
                    is_enrolled_program = True
                    break

        #grant access if enrolled to either the course or the program or user owns the moudle
        obj = obj
        if is_enrolled_course or is_enrolled_program or (module_owner == requester):
            return Response({"message": "Allowed"})
        else:
            if not is_enrolled_course:
                
                if user_profile.creator:
                    message = f"Access Denied. You do not own the course or program this {obj} belongs to."
                    return Response({"message": message})
                message = "You are not enrolled in the course or program."  
                return Response({"message": message})
            else:
                message = f"You do not have permission to access this {obj}."
                return Response({"message":message})
            
class ModuleDetailAPIView(generics.RetrieveAPIView):

    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticated]
    
    #check if the requester is enrolled or owns the module if so grant access
    def get(self, request, *args, **kwargs):
        
        module = self.get_object()

        response = isEnrolledOrOwner(module, request, 'module')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if response.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return response

class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer 
    permission_classes = [IsAuthenticated]

class ModuleCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    # create  module assign it to a course and update course info
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            course_name = serializer.validated_data['course']
            try:
                course = Course.objects.get(name=course_name)
            except Course.DoesNotExist:
                return Response({"error": "course does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if course.owner == self.request.user: 
                Module.objects.create(owner=self.request.user, course=course, name=name, created_at=date)  
                num_modules = course.number_of_modules          #update number of modules field to reflect chnage
                num_modules += Decimal(1)
                course.number_of_modules = num_modules
                course.save()
                return Response({"message": "module created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)

class MediaCreateAPIView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer

class ModuleUpdateAPIView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this module.")
        return super().update(request, *args, **kwargs)
class MediaUpdateAPIView(generics.UpdateAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this media.")
        return super().update(request, *args, **kwargs)

class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        instance.delete()
        return Response({"message": "Module deleted successfully."},
                        status=status.HTTP_200_OK)
    
class MediaDestroyAPIView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        instance.delete()
        return Response({"message": "Media deleted successfully."},
                        status=status.HTTP_200_OK)
    
