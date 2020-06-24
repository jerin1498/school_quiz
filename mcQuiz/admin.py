from django.contrib import admin
from .models import Subject, Question, ExamPaper


# Register your models here.

class AdminSubject(admin.ModelAdmin):
    list_filter = ['subject', ]
    search_fields = ['subject', 'question__question']
    fields = ['subject', 'question', 'no_of_questions_to_ask', 'number_of_questions_selected',
              'ask_random_questions', 'session_name']
    readonly_fields = ['number_of_questions_selected', ]
    list_display = ['subject', 'number_of_questions_selected', 'no_of_questions_to_ask', 'ask_random_questions']

    class Meta:
        model = Subject


class AdminQuestion(admin.ModelAdmin):
    search_fields = ['question',]
    list_display = ['question', 'choice_A', 'choice_B', 'choice_C', 'choice_D']


admin.site.register(Subject, AdminSubject)
admin.site.register(Question, AdminQuestion)
admin.site.register(ExamPaper)


