from datetime import datetime
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from permissions import IsContentCreator
from .models import *
from .serializers import *
from decimal import Decimal
from quiz.models import Grade
from utils import enrolled_owner

# Create your views here.
class QuizDetailAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsAuthenticated]

    #can a  see the quiz if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        quiz = self.get_object()
        module = quiz.module
        user = request.user
        respone = enrolled_owner(module, user, 'quiz')
        
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
    def create(self, request, module_id, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        date_today = date.today()
        user = request.user
        response = Quiz.create_quiz(module_id, serializer, date_today, user)
        return response
        

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
    
class QuizDestroyAPIView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerialzer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()

        # Check ownership
        if instance.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this quiz.")
        
        #adjust module to reflect current change
        module = instance.module
        num_quizs = module.num_quizs
        num_quizs -= Decimal(1)
        module.num_quizs = num_quizs
        module.save()

        instance.delete()
        return Response({"message": "Quiz deleted successfully."},
                        status=status.HTTP_200_OK)


class QuestionCreateAPIView(generics.CreateAPIView):
    """
    create a question, multiple choice(multi=True) and answer being choice number(eg:choice_1).
    or a blank space question, answer being a string(eg: "this is an answer").
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator] 

    # create  Quiz assign it to a module
    def create(self, request, quiz_id, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            multi = serializer.validated_data['multi']      #ethier "True" or "False"
            answer = serializer.validated_data['answer']    #string of actual of answer or choice
            value = serializer.validated_data['value']
            
            try:
                quiz = Quiz.objects.get(id=quiz_id)
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

class QuestionDetailAPIView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    #can a  see the quiz if user is learner that is enrolled or owns the module
    def get(self, request, *args, **kwargs):
        
        question = self.get_object()
        quiz = question.quiz
        module = quiz.module
        user = request.user
        respone = enrolled_owner(module, user, 'question')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone
        
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
    
        
class QuestionDestroyAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
        instance = self.get_object()
        quiz = question.quiz
        
        # Check ownership
        if quiz.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this Question.")
        instance.delete()
        return Response({"message": "Question deleted successfully."},
                        status=status.HTTP_200_OK)

    
class AnswerCreateAPIView(generics.CreateAPIView):
    """
    create an answer, for multiple choice question(multi=True) can have multiple possible answers for a questoin 
    for blank space question only one answer.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator] 

    # create  Quiz assign it to a module 
    def create(self, request, question_id, *args, **kwargs):
        date = datetime.now()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            choice_number = serializer.validated_data['choice_number']
            value = serializer.validated_data['value']    #string of actual of answer or choice
            
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return Response({"error": "question does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            #check if choice number aleardy exists in the choices for the question
            contains = question.choices.filter(choice_number__exact=choice_number)
            if contains:
                return Response({"error": "choice number already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

            # create answer only if user owns the module the quiz belongs to and question is multi
            quiz= question.quiz
            module = quiz.module
            if module.owner == self.request.user and question.multi: 
                #try:
                #except IntegrityError:
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
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

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
        user = request.user
        respone = enrolled_owner(module, user, 'answer')
        
        #grant access if enrolled to either the course or the program or user owns the moudle
        if respone.data['message'] == 'Allowed':
            return super().get(request, *args, **kwargs)
        else:
            return respone
                    
class AnswerUpdateAPIView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        question = instance.question
        quiz = question.quiz
        # Check ownership
        if quiz.owner != request.user:
            raise PermissionDenied("You do not have permission to edit this answer.")
            
        if serializer.is_valid():
            #check if choice number aleardy exists in the choices for the question
            if 'choice_number' in serializer.validated_data:
                choice_number = serializer.validated_data['choice_number'] 
                contains = question.choices.filter(choice_number__exact=choice_number)
                if contains:
                    return Response({"error": "choice number already exists."},
                                    status=status.HTTP_400_BAD_REQUEST)
                
                instance.choice_number = serializer.validated_data['choice_number']

            else:
                instance.choice_number =  instance.choice_number

            if 'value' in serializer.validated_data:
                instance.value = serializer.validated_data['value']
            else:
                instance.value = instance.value
            
            instance.save()
            return Response({'message': 'Update successful'}, 
                            status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AnswerDestroyAPIView(generics.DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsContentCreator]

    def destroy(self,request, *args, **kwargs):
    
        instance = self.get_object()
        question = instance.question
        quiz = question.quiz
        
        # Check ownership
        if quiz.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this answer.")
        instance.delete()
        return Response({"message": "answer deleted successfully."},
                        status=status.HTTP_200_OK)
    
class SubmitAnswersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id, learner_id):
        #validate
        response = Answer.validate(learner_id, quiz_id, request)
        if response.data['error']:
            return response
        learner = response.data['learner']
        answers = response.data['answers']
        module = response.data['module']
        quiz = response.data['quiz']
        questions_count = response.data['questions_count']
        #calculate score
        grade = Answer.score_answers(answers, learner, questions_count)
        #regitser grade
        response = Grade.register_grade(grade, module,learner, quiz)
        return response