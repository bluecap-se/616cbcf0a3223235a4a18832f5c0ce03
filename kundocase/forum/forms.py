from django import forms

from kundocase.forum import models


class QuestionForm(forms.ModelForm):

    class Meta:
        model = models.Question
        exclude = ['created', 'updated']
        widgets = {
        }


class AnswerForm(forms.ModelForm):

    class Meta:
        model = models.Answer
        exclude = ['created', 'updated']
        widgets = {
            'question': forms.HiddenInput(),
        }
