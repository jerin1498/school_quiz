from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save
from quizMain.utils import unique_slug_generator
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Question(models.Model):
    question = models.TextField(help_text='Type the questions that you want to ask', unique=True)
    choice_A = models.CharField(max_length=120, help_text='choices for the questions this field is required')
    is_choice_A_correct = models.BooleanField('mark if the choice A is correct')
    choice_B = models.CharField(max_length=120, help_text='choices for the question this field is required')
    is_choice_B_correct = models.BooleanField('mark if the choice B is correct')
    choice_C = models.CharField(max_length=120, help_text='choices for the question this field is required')
    is_choice_C_correct = models.BooleanField('mark if the choice C is correct')
    choice_D = models.CharField(max_length=120, help_text='choices for the question this field is required')
    is_choice_D_correct = models.BooleanField('mark if the choice D is correct')

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    explanation = models.TextField(max_length=2000,
                                   blank=True,
                                   null=True,
                                   help_text="Explanation to be shown after the question has been answered.",
                                   verbose_name='Explanation')

    def __str__(self):
        return str(self.question)



    def clean(self, *args, **kwargs):
        choice_A = self.is_choice_A_correct
        choice_B = self.is_choice_B_correct
        choice_C = self.is_choice_C_correct
        choice_D = self.is_choice_D_correct
        print(choice_A, choice_B, choice_C, choice_D)
        if not(choice_A or choice_B or choice_C or choice_D):
            raise ValidationError('must mark any one correct choice')
        return super(Question, self).clean()


class Subject(models.Model):
    subject = models.CharField(max_length=50, unique=True, help_text='title of the quiz')
    question = models.ManyToManyField(Question)
    ask_random_questions = models.BooleanField(help_text='mark if you want to ask random questions, '
                                                         'question order will be shuffled')
    no_of_questions_to_ask = models.PositiveIntegerField(default=10, help_text='select no of questions '
                                                                       'that you want to ask the exam')
    slug = models.SlugField(blank=True, unique=True)
    session_name = models.CharField(unique=True, max_length=120, help_text='this field is used to avoid the user to '
                                                                           're-attend the same exam')
    has_session = models.BooleanField(default=False)

    def __str__(self):
        return str(self.subject)

    @property
    def number_of_questions_selected(self):
        subject_class = self.__class__
        filter_subject_qs = subject_class.objects.filter(subject=self.subject)
        subject_obj = filter_subject_qs.first()
        total_questions_selected = subject_obj.question.all().count()
        return str(total_questions_selected)

    def get_absolute_url(self):
        return reverse('quiz:exam', kwargs={'slug': self.slug})


def subject_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(subject_pre_save_receiver, sender=Subject)


class ExamPaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_detail = models.TextField()
    question_asked = models.TextField()

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        pass





