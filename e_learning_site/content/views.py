from datetime import datetime
from django.shortcuts import render, redirect
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsContentCreator, IsLearner, IsLearnerOrContentCreater
from .models import *
from user.models import CourseEnrollment, ProgramEnrollment, UserProfile
from .serializers import *
from decimal import Decimal

class MarkAsComplete(APIView):
    """
    given the module NAME mark it as completed and update overal progress on the program or course.
    """
    permission_classes = [IsLearnerOrContentCreater]

    def update_module(self, module_course, enrollment):
        num_modules = module_course.number_of_modules
        completed = enrollment.number_of_modules_completed
        progress = (completed / num_modules) * 100
        enrollment.progress = progress
        enrollment.save()

    def patch(self, request):
        date = datetime.now()
        serializer = MarkAsCompleteSerializer(data=request.data)
        if serializer.is_valid():
            module_name = serializer.validated_data['module']
            user = self.request.user
            user_profile = UserProfile.objects.get(user=user)
            try:
                module = Module.objects.get(name=module_name)
            except Module.DoesNotExist:
                return Response({"message":"module does not exist"})
            
            #update module
            module.completed = True
            module.completed_at = date
            # check progress
            module_course = module.course
            try:
                course_program = Program.objects.get(courses__name=module_course.name)
            except Program.DoesNotExist:
                # course not parrt of a program
                try:
                    enrollment = CourseEnrollment.objects.get(Q(learner=user_profile) & Q(course=module_course))
                except CourseEnrollment.DoesNotExist:
                    if user == module_course.owner:
                        self.update_module(module_course, enrollment)
                    else:
                        return Response({"message":"You do not have permission to perform this action"})
                
                self.update_module(module_course, enrollment)
                return Response({"message":"module marked as complet successfully"})
                

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

            
            CourseEnrollment.objects.create(learner=learner_profile, course=course, date_of_enrollment=date)
            return Response({"message":"Application to program accepted succesfully"})
                
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
            
class Enroll(APIView):
    pass
               
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

                    return redirect('add_course-view')
                else:
                    return Response({"message": "you do not have permission to perform this action"})
            else:
               return Response({"message": "course or program does not exist"})
               
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

class ModuleDetailAPIView(generics.RetrieveAPIView):

    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'
    #check if the requester is enrolled or owns the module if so grant access
    def get(self, request, *args, **kwargs):

        module = self.get_object()
        module_owner = module.owner
        modules_course = module.course
        requester = self.request.user
        user_profile = UserProfile.objects.get(user=requester)
            
        try:
            CourseEnrollment.objects.get(Q(course=modules_course) & Q(learner=user_profile))
            isEnrolled = True
        except CourseEnrollment.DoesNotExist:
            isEnrolled = False
        
        if isEnrolled or (module_owner == requester):
            return super().get(request, *args, **kwargs)
        else:
            return Response({"message":"You are not enrolled in the course."})


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
        serializer.save(owner=self.request.user)

    
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ModuleCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        date = datetime.now()
        if serializer.is_valid():
            name = serializer.validated_data['name']
            course_name = serializer.validated_data['course']
            try:
                course = Course.objects.get(name=course_name)
            except ObjectDoesNotExist:
                return Response({"message": "course does not exist"})

            if course.owner == self.request.user: 
                Module.objects.create(owner=self.request.user, course=course, name=name, created_at=date)  
                num_modules = course.number_of_modules #update number of modules field to reflect chnage
                num_modules += Decimal(1)
                course.number_of_modules = num_modules
                course.save()
                return Response({"message": "module created succesfully"})
            else:
                return Response({"message": "you do not have permission to perform this action"})


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
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    

class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    

class MediaListAPIView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    

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

    
    
class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerialzer
    permission_classes = [IsContentCreator]
    

class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerialzer
    permission_classes = [IsContentCreator]
    

class MediaDestroyAPIView(generics.DestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]
    

class ApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]
    


