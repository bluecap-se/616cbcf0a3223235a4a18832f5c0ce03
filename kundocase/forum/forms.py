from django.forms import ModelForm

from kundocase.forum import models


class QuestionForm(ModelForm):

    class Meta:
        model = models.Question
        exclude = ['created', 'updated']
        widgets = {
        }


class AnswerForm(ModelForm):

    class Meta:
        model = models.Answer
        exclude = ['created', 'updated']
        widgets = {
        }
