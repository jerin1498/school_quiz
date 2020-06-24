from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Subject, ExamPaper
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
# Create your views here.


class QuizList(ListView): # displaying questions
    template_name = "mcQuiz/list.html"

    def get_queryset(self, *args, **kwargs):
        qs = Subject.objects.all()
        for no in range(qs.count()): # checking sessions
            obj = qs[no]
            session_name = obj.session_name
            try:
                req_session = self.request.session.get(str(session_name), None)
            except:
                req_session = None
            if req_session:
                obj.has_session = True
                obj.save()
            else:
                obj.has_session = False
                obj.save()
        return qs


class QuizExam(LoginRequiredMixin, View):  # asking questions
    login_url = '/account/login'

    def get(self, request, *args, **kwargs):
        subject = self.kwargs.get('slug')
        subject_obj = Subject.objects.filter(subject=subject).first()
        try:
            session_name = subject_obj.session_name
        except:
            session_name = None
        sess = request.session.get(str(session_name), None)
        if sess == session_name: # checking weather the user attend the exam or not
            return redirect('/quiz/result')
        request.session.set_expiry(864000) # for 10 days
        request.session[str(session_name)] = session_name

        no_of_questions_available = subject_obj.question.all().count()
        if subject_obj.no_of_questions_to_ask == 0:
            no_of_questions_to_ask = 1
        else:
            no_of_questions_to_ask = subject_obj.no_of_questions_to_ask

        if no_of_questions_available >= no_of_questions_to_ask: # setting how many questions to ask
            print('questions are there')
            limit = no_of_questions_to_ask
        else:
            limit = no_of_questions_available

        if subject_obj.ask_random_questions:
            questions = subject_obj.question.all().order_by('?')[0:limit]

        else:
            questions = subject_obj.question.all()
        questions_obj = []
        for question in questions: #converting qs into dict so we can use in front end easyly .
            temp_question = {}
            temp_question['question'] = question.question
            temp_question['choice_A'] = question.choice_A
            temp_question['is_choice_A_correct'] = question.is_choice_A_correct
            temp_question['choice_B'] = question.choice_B
            temp_question['is_choice_B_correct'] = question.is_choice_B_correct
            temp_question['choice_C'] = question.choice_C
            temp_question['is_choice_C_correct'] = question.is_choice_C_correct
            temp_question['choice_D'] = question.choice_D
            temp_question['is_choice_D_correct'] = question.is_choice_D_correct
            if question.explanation:
                temp_question['explanation'] = question.explanation
            else:
                temp_question['explanation'] = None
            questions_obj.append(temp_question)
        json_questions = json.dumps(questions_obj)

        context = {'object': subject_obj, 'questions': json_questions}
        return render(request, "mcQuiz/exam.html", context)


class SaveExamResult(LoginRequiredMixin, View):  # saving the user result
    login_url = '/account/login'

    def post(self, request, *args, **kwargs):
        exam_paper = request.POST.get('save-answer-value', None)
        exam_detail = request.POST.get('save-exam-detail', None)
        user = request.user
        exam_obj = ExamPaper.objects.create(user=user, exam_detail=exam_detail, question_asked=exam_paper)
        exam_obj.save()
        context = {}
        return redirect('/quiz/result')


class ResultList(LoginRequiredMixin, ListView): # displaying the user result
    login_url = '/account/login'
    template_name = 'mcQuiz/result_list.html'

    def get_queryset(self):
        request = self.request
        user = request.user
        qs = ExamPaper.objects.filter(user=user)
        return qs

    def get_context_data(self, **kwargs):
        context =super(ResultList, self).get_context_data(**kwargs)
        exam_list = []
        request = self.request
        user = request.user
        qs = ExamPaper.objects.filter(user=user)
        for subject in qs:
            exam_obj = subject.exam_detail
            exam_list.append(exam_obj)

        context['exam_detail'] = json.dumps(exam_list)
        return context


