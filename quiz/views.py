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
from quiz.models import Grade
from application.serializers import ApplicationSerialzer
from module.views import isEnrolledOrOwner

# Create your views here.
class QuizDetailAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsAuthenticated]

    #can a  see the quiz if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        quiz = self.get_object()
        module = quiz.module
        respone = isEnrolledOrOwner(module, request, 'quiz')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone

class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    #can a  see the quiz if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        question = self.get_object()
        quiz = question.quiz
        module = quiz.module
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

    #can a  see the quiz if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        answer = self.get_object()
        question = answer.question
        quiz = question.quiz
        module = quiz.module
        respone = isEnrolledOrOwner(module, request, 'answer')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone
        
class QuizCreateAPIView(generics.CreateAPIView):

    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsContentCreator] 

    # create  Quiz assign it to a module
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            description = serializer.validated_data['description']
            pass_score = serializer.validated_data['pass_score']
            id = request.data.pop('module_id', None)
            try:
                module = Module.objects.get(id=int(id))
            except Module.DoesNotExist:
                return Response({"error": "module does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if module.owner == self.request.user: 
                Quiz.objects.create(owner=self.request.user, 
                                    module=module, 
                                    description=description,
                                    pass_score=pass_score, 
                                    created_at=date)  
                num_quizs = module.num_quizs
                num_quizs += Decimal(1)
                module.numquizs = num_quizs
                module.save()
                return Response({"message": "quiz created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid serializer."},
                            status=status.HTTP_400_BAD_REQUEST)
        
class QuestionCreateAPIView(generics.CreateAPIView):
    """
    create a question, multiple choice(multi=True) and answer being choice number(eg:choice_1).
    or blank space question answer being a string(eg: "this is an answer").
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator] 

    # create  Quiz assign it to a module
    def create(self, request, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            multi = serializer.validated_data['multi']      #ethier "True" or "False"
            answer = serializer.validated_data['answer']    #string of actual of answer or choice
            value = serializer.validated_data['value']
            id = request.data.pop('quiz_id', None)
            try:
                quiz = Quiz.objects.get(id=int(id))
            except Quiz.DoesNotExist:
                return Response({"error": "quiz does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            # create question only if user owns the module the quiz belongs to
            module = quiz.module
            if module.owner == self.request.user: 
                Question.objects.create(quiz=quiz, value=value,
                                        multi=bool(multi),
                                        answer=answer,
                                        created_at=date)
                
                #update number of qestions in the quiz
                num_of_questions = quiz.num_of_questions 
                num_of_questions += Decimal(1)
                quiz.num_of_questions = num_of_questions
                quiz.save()
                return Response({"message": "question created succesfully"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "you do not have permission to perform this action"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid serializer."},
                            status=status.HTTP_400_BAD_REQUEST)

class AnswerCreateAPIView(generics.CreateAPIView):
    """
    create an answer, for multiple choice question(multi=True) can have multiple possible answers for a questoin 
    for blank space question only one answer.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator] 

    # create  Quiz assign it to a module
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
                return Response({"error": "question does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            # create answer only if user owns the module the quiz belongs to and question is multi
            quiz= question.quiz
            module = quiz.module
            if module.owner == self.request.user and question.multi: 
                Answer.objects.create(question=question,
                                      value=value,
                                    choice_number=choice_number,
                                    created_at=date)  
                
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

    def post(self, request, quiz_id, learner_id):
        
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except (Quiz.DoesNotExist):
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            learner = User.objects.get(id=learner_id)
        except User.DoesNotExist:
            return Response({"error": "learner not found"}, status=status.HTTP_404_NOT_FOUND)
        
        module = quiz.module
        response = isEnrolledOrOwner(module, request, "quiz")
        if response.data['message'] == 'Allowed'  and (learner == request.user):
            # Assume the request data contains the answers for each question
            answers = request.data.get('answers', [])
            correct_count = 0
            questions_count = quiz.num_of_questions

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
            
            if grade >= quiz.pass_score:
                #update grade records
                Grade.objects.create(module=module, quiz=quiz, learner=learner,grade=grade, passed=True)
            else:
                #update grade records
                Grade.objects.create(module=module, quiz=quiz, learner=learner,grade=grade, passed=False)

            return Response({
                "learner": learner.first_name,
                "correct_answers": correct_count,
                "total_questions": questions_count,
                "grade": grade
            }, status=status.HTTP_200_OK)
        else:
            return  Response({
                "message":"can not perform this action."
            }, status=status.HTTP_403_FORBIDDEN)
        
class QuizListAPIView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsContentCreator]

    #owners of quizs can list all their quizs
    def filter_queryset(self, query_set):
        owner = self.request.user
        return Quiz.objects.filter(owner=owner)

class QuizUpdateAPIView(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        return super().update(request, *args, **kwargs)
class QuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator]

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        quiz = instance.quiz
        # Check ownership
        if quiz.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this question.")
        return super().update(request, *args, **kwargs)
    
class AnswerUpdateAPIView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        question = instance.question
        quiz = question.quiz
        # Check ownership
        if quiz.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this answer.")
        return super().update(request, *args, **kwargs)
    
class QuizDestroyAPIView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
    
        # Check ownership
        if instance.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        instance.delete()
        return Response({"message": "Quiz deleted successfully."},
                        status=status.HTTP_200_OK)

class QuestionDestroyAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator]

    def perform_destroy(self,instance):
        instance = self.get_object()
        quiz = instance.quiz
        module = quiz.module
        # Check ownership
        if module.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this quiz.")
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
        quiz = question.quiz
        module = quiz.module
        # Check ownership
        if module.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this answer.")
        instance.delete()
        return Response({"message": "answer deleted successfully."},
                        status=status.HTTP_200_OK)
    