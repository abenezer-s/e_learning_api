from datetime import datetime, date, timedelta
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
from test.models import Grade
from application.serializers import ApplicationSerialzer
from module.views import isEnrolledOrOwner

# Create your views here.
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
                return Response({"message": "module does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if module.owner == self.request.user: 
                Test.objects.create(owner=self.request.user, module=module, description=description,time_limit=time_limit, pass_score=pass_score, created_at=date)  
                num_tests = module.num_tests
                num_tests += Decimal(1)
                module.numtests = num_tests
                module.save()
                return Response({"message": "test created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Invalid serializer."},
                            status=status.HTTP_400_BAD_REQUEST)
        
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
                return Response({"message": "test does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            # create question only if user owns the module the test belongs to
            module = test.module
            if module.owner == self.request.user: 
                Question.objects.create(test=test, value=value, multi=bool(multi),answer=answer, created_at=date)
                #update number of qestions in the test
                num_of_questions = test.num_of_questions 
                num_of_questions += Decimal(1)
                test.num_of_questions = num_of_questions
                test.save()
                return Response({"message": "question created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Invalid serializer."},
                            status=status.HTTP_400_BAD_REQUEST)

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
                return Response({"message": "question does not exist"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # create answer only if user owns the module the test belongs to and question is multi
            test= question.test
            module = test.module
            if module.owner == self.request.user and question.multi: 
                Answer.objects.create(question=question, value=value, choice_number=choice_number, created_at=date)  
                return Response({"message": "answer created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                if not question.multi:
                    return Response({"error": "question not multiple choice."},
                                    status=status.HTTP_400_BAD_REQUEST)    
                
                return Response({"message": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Invalid serializer.",
                             "error": serializer.errors},
                             status=status.HTTP_400_BAD_REQUEST)
                

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
        
class TestListAPIView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator]

    #owners of tests can list all their tests
    def filter_queryset(self, query_set):
        owner = self.request.user
        return Test.objects.filter(owner=owner)

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
    
class TestDestroyAPIView(generics.DestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this test.")
        instance.delete()
        return Response({"message": "Test deleted successfully."},
                        status=status.HTTP_200_OK)

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
        return Response({"message": "question deleted successfully."},
                        status=status.HTTP_200_OK)
    
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
        return Response({"message": "answer deleted successfully."},
                        status=status.HTTP_200_OK)
    