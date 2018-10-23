from django.core.exceptions import ValidationError
from django.db import models
from kundocase.forum.spamcheck import SpamCheck


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        if self.user_email == self.user_name:
            raise ValidationError('User name and email can not be the same.')

        if SpamCheck(self).has_spam():
            raise ValidationError('Content contains spam.')

        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        if self.user_email == self.user_name:
            raise ValidationError('User name and email can not be the same.')

        if SpamCheck(self).has_spam():
            raise ValidationError('Content contains spam.')

        super(Answer, self).save(*args, **kwargs)
