from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsContentCreator, IsLearner, IsLearnerOrContentCreater
from .models import *
from user.models import CourseEnrollment, ProgramEnrollment, UserProfile
from .serializers import *
from decimal import Decimal
from rest_framework.parsers import MultiPartParser, FormParser


class MarkComplete(APIView):
    """
    Given the module, course and program name and learner username(string "None" if not part of program),
    mark the module as completed 
    and update overal progress on the program or course.
    """
    permission_classes = [IsLearnerOrContentCreater]

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

                        return Response({"message":"program completed successfully!",
                                         "score": prog_score})
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
            course_enrollment.status = 'complete'
            course_enrollment.save()
            
            return Response({"message":"course completed successfully! 2",
                            "score":format(course_score, '.2f')})
            
        elif cur_progress_course != 100:
            #learner has completed the module
            result = Grade.objects.get(module=module, learner=learner)
            score = result.grade
            
            LearnerCompletion.objects.get_or_create(learner=learner,
                                              module=module, 
                                              score=score, 
                                              completed_at=date)
            
            return Response({"message":"module completed successfully! 1",
                             "score":score})

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
            
            return Response({"message":"course completed successfully. 1",
                             "score": course_score})

    def patch(self, request, module_id, learner_id):
        
        user = self.request.user
        # get instances
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"message":"learner not found"})
        
        learner_profile = UserProfile.objects.get(user=learner)
        
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"message":"module does not exist"})
        #proceed if module not already completed

        try:
            LearnerCompletion.objects.get(module=module, learner=learner)
        except (LearnerCompletion.DoesNotExist):
            pass
        except LearnerCompletion.MultipleObjectsReturned:
            return Response({"messge":"Module already completed"})
        else:
            return Response({"messge":"Module already completed"})
            

        try:
            module_course = Course.objects.get(id=module.course.id) #course where the module belongs to
        except Module.DoesNotExist:
            return Response({"message":"module's course does not exist"}) 
        
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

        #check learner has passed all tests in module then update progress
        num_tests = module.num_tests
        tests_passed = 0
        passed_all_tests = None
        if num_tests > 0: 
            tests_passed = Grade.objects.filter(learner=learner, module=module, passed=True).count()
            
            if num_tests == tests_passed:
                passed_all_tests = True
               
            else:
                passed_all_tests= False
                return Response({"message":"can not mark module as complete. You have not passed all tests."})
        else:
            passed_all_tests = True
            #create a full score for module ensuring a module is always scored
            Grade.objects.get_or_create(learner=learner, module=module, grade=100, passed=True)

        #if learner is within deadline and is enrolled or user is owner of module update
        if (learner_profile.creator == False) or (user == module.owner):
            if is_enrolled_course and within_deadline and passed_all_tests:
                
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
                    return Response({"message":"you do not have permisssion to perform this action. Not enrolled."})
                else:
                    return Response({"message":"you can not perform this action. Deadline has passed."})
        else:
                return Response({"message":"you do not have permisssion to perform this action"})
                
            
class ApplicationResponse(APIView):
    """
    Provided with the program/course name, learner's username and a response, reject or accept application.
    
    Send a string None on program or course's field to apply to one of them.
    """   
    permission_classes = [IsContentCreator]
    def reject(self, learner, program_name, course_name, request, date):
        if course_name != "None":
            try:
                learner_obj = User.objects.get(username=learner)
                course = Course.objects.get(name=course_name)
                course_owner = course.owner
                if course_owner != request.user:
                    return Response({"message":"You do not have permission to perform this action"})
                
            except ObjectDoesNotExist:
                return Response({"message":"no course or learner found by the provided course or learner name"})
           
            try:
                application = Application.objects.get(Q(course=course) & Q(learner=learner_obj))
                application.state = 'rejected'
                application.save()
            except ObjectDoesNotExist:
                return Response({"message":"Application not found"})
    
            return Response({"message":"Application to course rejected succesfully"})
        
        else:
            try:
                learner_obj = User.objects.get(username=learner)
                program = Program.objects.get(name=program_name)
                program_owner = program.owner
                if program_owner != request.user:
                    return Response({"message":"You do not have permission to perform this action"})
            except ObjectDoesNotExist:
                return Response({"message":"no program or learner found by the provided program or program name"})

            try:
                application = Application.objects.get(Q(program=program) & Q(learner=learner_obj))  
            except Application.DoesNotExist:
                return Response({"message":"Application not found"})
            
            application.state = 'rejected'
            application.save()
            return Response({"message":"Application to program rejected succesfully"})

    def accept(self, learner, program_name, course_name, request, date):
        #response for course  
        if course_name != 'None':
            try:
                learner_obj = User.objects.get(username=learner)
                learner_profile = UserProfile.objects.get(user=learner_obj)
                course = Course.objects.get(name=course_name)
                course_owner = course.owner
                if course_owner != request.user:
                    return Response({"message":"You do not have permission to perform this action"})
                
            except ObjectDoesNotExist:
                return Response({"message":"no course or learner found by the provided course or learner name"})
            try:
                application = Application.objects.get(Q(course=course) & Q(learner=learner_obj))
                application.state = 'accepted' # needs fixing
                application.save()
            except ObjectDoesNotExist:
                return Response({"message":"Application not found"})

            #enroll learner to course with appropriate deadlines if there are any
            num_weeks = course.complete_within
            if num_weeks:
                deadline = date + timedelta(weeks=num_weeks)
                CourseEnrollment.objects.create(learner=learner_profile, course=course, date_of_enrollment=date, deadline=deadline)
            else:
                CourseEnrollment.objects.create(learner=learner_profile, course=course, date_of_enrollment=date)
                
            return Response({"message":"Application to program accepted succesfully"})

        #response for program                
        else:
            try:
                learner_obj = User.objects.get(username=learner)
                learner_profile = UserProfile.objects.get(user=learner_obj)
                program = Program.objects.get(name=program_name)
                program_owner = program.owner
                if program_owner != request.user:
                    return Response({"message":"You do not have permission to perform this action"})
            except ObjectDoesNotExist:
                return Response({"message":"no program or learner found by the provided program or program name"})
            
            try:
                application = Application.objects.get(Q(program=program) & Q(learner=learner_obj))
                application.state = 'accepted' 
                application.save()
            except ObjectDoesNotExist:
                return Response({"message":"Application not found"})
            
            #enroll learner to program with appropriate deadlines if there are any
            num_weeks = program.complete_within
            if num_weeks:
                deadline = date + timedelta(weeks=num_weeks)
                ProgramEnrollment.objects.create(learner=learner_profile, program=program, date_of_enrollment=date, deadline=deadline)
            else:
                ProgramEnrollment.objects.create(learner=learner_profile, program=program, date_of_enrollment=date)

            return Response({"message":"Application to program accepted succesfully"})

    def post(self, request):
        date = datetime.now()
        serializer = ApplicationResponseSerializer(data=request.data)
        if serializer.is_valid():
            learner = serializer.validated_data['learner']
            program_name = serializer.validated_data['program_name']
            course_name = serializer.validated_data['course_name']
            response = serializer.validated_data['response']
            if response not in ['Accept', 'Reject']:
                return Response({"message":"response not recognized. Must be Accept or Reject."})
            
            #enroll learner to course/program if accepted            
            if response == 'Accept':
                response = self.accept(learner, program_name, course_name, request, date)
                return response
            else:
                self.reject(learner, program_name, course_name, request, date)
                return Response({"message":"Application rejected succesfully"})
        else:
                    
            pass

class Apply(APIView):
    """
    learner passes in application information for a course or program, 
    an Application instance will be created conatining the info.
    """
    permission_classes = [IsLearner]
    def post(self, request):
        date = datetime.now()
        serializer = ApplySerializer(data=request.data)
        if serializer.is_valid():
            learner = serializer.validated_data['learner']
            motivation_letter = serializer.validated_data['motivation_letter']
            program_name = serializer.validated_data['program_name']
            course_name = serializer.validated_data['course_name']

            if course_name != 'None':
                try:
                    course = Course.objects.get(name=course_name)
                except Course.DoesNotExist:
                    return Response({"message":"course not found"})
                course_owner = course.owner
                try:
                    learner_user = User.objects.get(username=learner)
                except User.DoesNotExist:
                    return Response({"message":"User not found"})
                try:
                    application = Application.objects.create(owner=course_owner, learner=learner_user,submitted_at=date, motivation_letter=motivation_letter, state='Pending')
                except Application.DoesNotExist:
                    return Response({"message":"application not found"})
                application.course.add(course)
                return Response({"message":"successfully applied to course"})
            else:
                try:
                    program = Program.objects.get(name=program_name)
                except Program.DoesNotExist:
                    return Response({"message":"program not found"})
                program_owner = program.owner
                try:
                    learner_user = User.objects.get(username=learner)
                except User.DoesNotExist:
                    return Response({"message":"User not found"})
                try:
                    application = Application.objects.create(owner=program_owner, learner=learner_user,submitted_at=date, motivation_letter=motivation_letter, state='Pending')
                except Application.DoesNotExist:
                    return Response({"message":"application not found"})
                application.program.add(program)
                return Response({"message":"successfully applied to program"})
            
        print(serializer.errors)
        return Response({"message":"invalid serializer"})
                   
class AddCourseAPIView(APIView):
   """
   Providing course and program name as JSON, add course to the program if user owns both the course and the program
   """
   permission_classes = [IsContentCreator]

   def post(self, request):
       serializer = AddCourseSerializer(data=request.data)
       if serializer.is_valid():
            course_name = serializer.validated_data['course']
            program_name = serializer.validated_data['program']
            course = Course.objects.get(name=course_name)
            program = Program.objects.get(name=program_name)
            if (course and program):
                if course.owner == program.owner == request.user:   
                    program.courses.add(course)
                    num_courses = program.number_of_courses #update number of courses field to reflect chnage
                    num_courses += Decimal(1)
                    program.number_of_courses = num_courses
                    program.save()

                    return redirect('add-course-view')
                else:
                    return Response({"message": "you do not have permission to perform this action"})
            else:
               return Response({"message": "course or program does not exist"})

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
                return Response({"message":"Can not add media to module. Module does not exist."})
        
            #create media instance if user owns the module
            if user == module.owner:
                Media.objects.create(owner=user, file=file, description=description, module=module)
                return Response({"message":"Added media to module successfully."})
            else: 
                return Response({"message":"Can not add media to module. You do not have permission."})
        else:
            e = serializer.errors
            return Response({"message":"Invalid serializer.",
                             "error":e})

#detail views
class ProgramDetailAPIView(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

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

class TestDetailAPIView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsAuthenticated]

    #can a  see the test if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        test = self.get_object()
        module = test.module
        respone = isEnrolledOrOwner(module, request, 'test')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone

class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    #can a  see the test if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        question = self.get_object()
        test = question.test
        module = test.module
        respone = isEnrolledOrOwner(module, request, 'question')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone
        
class AnswerDetailAPIView(generics.RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    #can a  see the test if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        question = answer.question
        test = question.test
        module = test.module
        respone = isEnrolledOrOwner(module, request, 'answer')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone
        
class MediaDetailAPIView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer 
    permission_classes = [IsAuthenticated]

class ApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticated]

#create views

class ProgramCreateAPIView(generics.CreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] # need to be a content creator to create a program
    
    def perform_create(self, serializer):
        #assign user as an owner
        date = datetime.now()
        serializer.save(owner=self.request.user, created_at=date)

class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        date = datetime.now()
        serializer.save(owner=self.request.user, created_at=date)

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
                return Response({"message": "course does not exist"})
            
            if course.owner == self.request.user: 
                Module.objects.create(owner=self.request.user, course=course, name=name, created_at=date)  
                num_modules = course.number_of_modules          #update number of modules field to reflect chnage
                num_modules += Decimal(1)
                course.number_of_modules = num_modules
                course.save()
                return Response({"message": "module created succesfully"})
            else:
                return Response({"message": "you do not have permission to perform this action"})

class TestCreateAPIView(generics.CreateAPIView):

    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator] 

    # create  Test assign it to a module
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            description = serializer.validated_data['description']
            time_limit = serializer.validated_data['time_limit']
            pass_score = serializer.validated_data['pass_score']
            id = request.data.pop('module_id', None)
            try:
                module = Module.objects.get(id=int(id))
            except Module.DoesNotExist:
                return Response({"message": "module does not exist"})
            
            if module.owner == self.request.user: 
                Test.objects.create(owner=self.request.user, module=module, description=description,time_limit=time_limit, pass_score=pass_score, created_at=date)  
                num_tests = module.num_tests
                num_tests += Decimal(1)
                module.numtests = num_tests
                module.save()
                return Response({"message": "test created succesfully"})
            else:
                return Response({"message": "you do not have permission to perform this action"})
        else:
            return Response({"message": "Invalid serializer."})
        
class QuestionCreateAPIView(generics.CreateAPIView):
    """
    create a question, multiple choice(multi=True) and answer being choice number(eg:choice_1).
    or blank space question answer being a string(eg: "this is an answer").
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator] 

    # create  Test assign it to a module
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            multi = serializer.validated_data['multi']      #ethier "True" or "False"
            answer = serializer.validated_data['answer']    #string of actual of answer or choice
            value = serializer.validated_data['value']
            id = request.data.pop('test_id', None)
            try:
                test = Test.objects.get(id=int(id))
            except Test.DoesNotExist:
                return Response({"message": "test does not exist"})
            
            # create question only if user owns the module the test belongs to
            module = test.module
            if module.owner == self.request.user: 
                Question.objects.create(test=test, value=value, multi=bool(multi),answer=answer, created_at=date)
                #update number of qestions in the test
                num_of_questions = test.num_of_questions 
                num_of_questions += Decimal(1)
                test.num_of_questions = num_of_questions
                test.save()
                return Response({"message": "question created succesfully"})
            else:
                return Response({"message": "you do not have permission to perform this action"})
        else:
            return Response({"message": "Invalid serializer."})

class AnswerCreateAPIView(generics.CreateAPIView):
    """
    create an answer, for multiple choice question(multi=True) can have multiple possible answers for a questoin 
    for blank space question only one answer.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator] 

    # create  Test assign it to a module
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            choice_number = serializer.validated_data['choice_number']
            value = serializer.validated_data['value']    #string of actual of answer or choice
            question_id = request.data.pop('question_id', None)
            try:
                question = Question.objects.get(id=int(question_id))
            except Question.DoesNotExist:
                return Response({"message": "question does not exist"})
            
            # create answer only if user owns the module the test belongs to and question is multi
            test= question.test
            module = test.module
            if module.owner == self.request.user and question.multi: 
                Answer.objects.create(question=question, value=value, choice_number=choice_number, created_at=date)  
                return Response({"message": "answer created succesfully"})
            else:
                if not question.multi:
                    return Response({"message": "question not multiple choice."})    
                
                return Response({"message": "you do not have permission to perform this action"})
        else:
            return Response({"message": "Invalid serializer.",
                             "error": serializer.errors})
                

class SubmitAnswersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, test_id, learner_id):
        
        try:
            test = Test.objects.get(id=test_id)
        except (Test.DoesNotExist):
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error": "learner not found"}, status=status.HTTP_404_NOT_FOUND)
        
        module = test.module
        response = isEnrolledOrOwner(module, request, "test")
        if response.data['message'] == 'Allowed'  and (learner == request.user):
            # Assume the request data contains the answers for each question
            answers = request.data.get('answers', [])
            correct_count = 0
            questions_count = test.num_of_questions

            #check answers' validity
            for answer_data in answers:
                try:
                    question = Question.objects.get(id=answer_data['question_id'])
                except Question.DoesNotExist:
                    continue  # Skip if the question does not exist

                submitted_ans = answer_data['submitted_ans']
                is_correct = (submitted_ans == question.answer)

                # Save the learner's answer
                LearnerAnswer.objects.create(learner=learner, question=question, answer=submitted_ans, correct=is_correct)

                if is_correct:
                    correct_count += 1

            # Calculate the grade percentage
            grade = round(float(correct_count) / float(questions_count), 2) * 100 if questions_count > 0 else 0
            
            if grade >= test.pass_score:
                #update grade records
                Grade.objects.create(module=module, test=test, learner=learner,grade=grade, passed=True)
            else:
                #update grade records
                Grade.objects.create(module=module, test=test, learner=learner,grade=grade, passed=False)

            return Response({
                "learner": learner.first_name,
                "correct_answers": correct_count,
                "total_questions": questions_count,
                "grade": grade
            }, status=status.HTTP_200_OK)
        else:
            return  Response({
                "message":"can not perform this action."
            }, status=status.HTTP_400_BAD_REQUEST)

class MediaCreateAPIView(generics.CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#list views
class ProgramListAPIView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category__name', 'duration']
    search_fields = ['name', 'owner__name']

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['category__name', 'duration']
    search_fields = ['name', 'owner__username']

    
class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer

class TestListAPIView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator]

    #owners of tests can list all their tests
    def filter_queryset(self, query_set):
        owner = self.request.user
        return Test.objects.filter(owner=owner)
    
class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerialzer
    
class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer

#update views
class ProgramUpdateAPIView(generics.UpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsContentCreator]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this program.")
        return super().update(request, *args, **kwargs)
        
class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsContentCreator]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this course.")
        return super().update(request, *args, **kwargs)

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

class TestUpdateAPIView(generics.UpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        return super().update(request, *args, **kwargs)
    
class QuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        test = instance.test
        # Check ownership
        if test.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this question.")
        return super().update(request, *args, **kwargs)
    
class AnswerUpdateAPIView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        question = instance.question
        test = question.test
        # Check ownership
        if test.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this answer.")
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

class ApplicationUpdateAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this application.")
        return super().update(request, *args, **kwargs)

#delete views
class ProgramDestroyAPIView(generics.DestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Program deleted successfully."})
    
class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsContentCreator]
    
    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Course deleted successfully."})

class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Module deleted successfully."})
    
class TestDestroyAPIView(generics.DestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Test deleted successfully."})

class QuestionDestroyAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
        instance = self.get_object()
        test = instance.test
        module = test.module
        # Check ownership
        if module.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this test.")
        instance.delete()
        return Response({"message": "question deleted successfully."})
    
class AnswerDestroyAPIView(generics.DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        instance = self.get_object()
        question = instance.question
        test = question.test
        module = test.module
        # Check ownership
        if module.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this answer.")
        instance.delete()
        return Response({"message": "answer deleted successfully."})
    
class MediaDestroyAPIView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Media deleted successfully."})
    

class ApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Media deleted successfully."})
    


