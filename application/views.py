from datetime import datetime, date, timedelta
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator, IsLearner
from .models import *
from users.models import CourseEnrollment, ProgramEnrollment, UserProfile
from .serializers import *
from application.serializers import ApplicationSerialzer

# Create your views here.
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
                    return Response({"error":"You do not have permission to perform this action"}, 
                                    status=status.HTTP_401_UNAUTHORIZED)
                
            except (User.DoesNotExist, Course.DoesNotExist):
                return Response({"error":"no course or learner found by the provided course or learner name"},
                                status=status.HTTP_404_NOT_FOUND)
           
            try:
                application = Application.objects.get(Q(course=course) & Q(learner=learner_obj))
                application.state = 'rejected'
                application.save()
            except Application.DoesNotExist:
                return Response({"error":"Application not found"},
                                status=status.HTTP_404_NOT_FOUND)
    
            return Response({"message":"Application to course rejected succesfully"}, 
                            status=status.HTTP_200_OK)
        
        else:
            try:
                learner_obj = User.objects.get(username=learner)
                program = Program.objects.get(name=program_name)
                program_owner = program.owner
                if program_owner != request.user:
                    return Response({"error":"You do not have permission to perform this action"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                
            except (User.DoesNotExist, Program.DoesNotExist):
                return Response({"error":"no program or learner found by the provided program or program name"},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                application = Application.objects.get(Q(program=program) & Q(learner=learner_obj))  
            except Application.DoesNotExist:
                return Response({"error":"Application not found"},
                                status=status.HTTP_404_NOT_FOUND)
            
            application.state = 'rejected'
            application.save()
            return Response({"message":"Application to program rejected succesfully"},
                            status=status.HTTP_200_OK)

    def accept(self, learner, program_name, course_name, request, date):
        #response for course  
        if course_name != 'None':
            try:
                learner_obj = User.objects.get(username=learner)
                learner_profile = UserProfile.objects.get(user=learner_obj)
                course = Course.objects.get(name=course_name)
                course_owner = course.owner
                if course_owner != request.user:
                    return Response({"error":"You do not have permission to perform this action"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                
            except (User.DoesNotExist, Course.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error":"no course or learner found by the provided course or learner name"},
                                status=status.HTTP_404_NOT_FOUND)
            try:
                application = Application.objects.get(Q(course=course) & Q(learner=learner_obj))
                
            except Application.DoesNotExist:
                return Response({"error":"Application not found"},
                                status=status.HTTP_200_OK)
            else:
                application.state = 'accepted' 
                application.save()

            #enroll learner to course with appropriate deadlines if there are any
            num_weeks = course.complete_within
            if num_weeks:
                deadline = date + timedelta(weeks=num_weeks)
                CourseEnrollment.objects.create(learner=learner_profile,
                                                course=course,
                                                date_of_enrollment=date, 
                                                deadline=deadline)
            else:
                CourseEnrollment.objects.create(learner=learner_profile,
                                                course=course,
                                                date_of_enrollment=date)
                
            return Response({"message":"Application to program accepted succesfully"},
                            status=status.HTTP_200_OK)

        #response for program                
        else:
            try:
                learner_obj = User.objects.get(username=learner)
                learner_profile = UserProfile.objects.get(user=learner_obj)
                program = Program.objects.get(name=program_name)
                program_owner = program.owner
                if program_owner != request.user:
                    return Response({"error":"You do not have permission to perform this action"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                
            except (User.DoesNotExist, Program.DoesNotExist, UserProfile.DoesNotExist):
                return Response({"error":"no program or learner found by the provided program or program name"},
                                status=status.HTTP_404_NOT_FOUND)
            
            try:
                application = Application.objects.get(Q(program=program) & Q(learner=learner_obj))
                
            except Application.DoesNotExist:
                return Response({"error":"Application not found"},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                application.state = 'accepted' 
                application.save()

            #enroll learner to program with appropriate deadlines if there are any
            num_weeks = program.complete_within
            if num_weeks:
                deadline = date + timedelta(weeks=num_weeks)
                ProgramEnrollment.objects.create(learner=learner_profile,
                                                program=program, 
                                                date_of_enrollment=date, 
                                                deadline=deadline)
            else:
                ProgramEnrollment.objects.create(learner=learner_profile, 
                                                 program=program, 
                                                 date_of_enrollment=date)

            return Response({"message":"Application to program accepted succesfully"},
                            status=status.HTTP_200_OK)

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
                accepted = self.accept(learner, program_name, course_name, request, date)
                return accepted
            else:
                self.reject(learner, program_name, course_name, request, date)
                return Response({"message":"Application rejected succesfully"},
                                status=status.HTTP_200_OK)
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
                    return Response({"error":"course not found"},
                                    status=status.HTTP_404_NOT_FOUND)
                course_owner = course.owner
                try:
                    learner_user = User.objects.get(username=learner)
                except User.DoesNotExist:
                    return Response({"error":"User not found"},
                                    status=status.HTTP_404_NOT_FOUND)
                
                application = Application.objects.create(owner=course_owner, 
                                                            learner=learner_user,
                                                            submitted_at=date,
                                                            motivation_letter=motivation_letter,
                                                            course=course,
                                                            state='Pending')
                
                return Response({"message":"successfully applied to course"},
                                status=status.HTTP_200_OK)
            else:
                try:
                    program = Program.objects.get(name=program_name)
                except Program.DoesNotExist:
                    return Response({"error":"program not found"},
                                    status=status.HTTP_404_NOT_FOUND)
                program_owner = program.owner
                try:
                    learner_user = User.objects.get(username=learner)
                except User.DoesNotExist:
                    return Response({"error":"User not found"},
                                    status=status.HTTP_404_NOT_FOUND)

                application = Application.objects.create(owner=program_owner,
                                                        learner=learner_user,
                                                        submitted_at=date,
                                                        motivation_letter=motivation_letter,
                                                        program=program,
                                                        state='Pending')

                
                return Response({"message":"successfully applied to program"},
                                status=status.HTTP_200_OK)
        else:    
            return Response({"error":"invalid serializer"},
                            status=status.HTTP_400_BAD_REQUEST)
    

class ApplicationDetailAPIView(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticated]

class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsAuthenticatedOrReadOnly, IsContentCreator] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer

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

class ApplicationDestroyAPIView(generics.DestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Media deleted successfully."},
                        status=status.HTTP_200_OK)
    