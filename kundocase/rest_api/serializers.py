import json

from django.core import serializers
from django.http import JsonResponse
from kundocase.forum import forms, models


class Serializer:

    def __init__(self, object=None):
        self.object = object
        self.data = None

    def to_representation(self, data):
        data = json.loads(serializers.serialize('json', data))
        self.data = [self.untaint(row) for row in data]

        return self.data

    def to_internal(self):
        # Validate with form.is_valid()
        pass

    def untaint(self, row):
        # Converts from {'fields': {'A': 'B'}} to {'A': 'B'}
        original = dict(row.get('fields', {}))

        # Check in `forms` which keys to include or exclude
        data = dict((k, original.get(k, None)) for k, _ in self.form.base_fields.items())

        # Append ID from parent
        data['id'] = row.pop('pk')

        return data

    def response(self, created=False):
        status = 200
        if created:
            status = 201
        elif not len(self.data):
            status = 404

        return JsonResponse(self.data, safe=False, status=status)


class QuestionSerializer(Serializer):
    form = forms.QuestionForm
    model = models.Question


class AnswerSerializer(Serializer):
    form = forms.AnswerForm
    model = models.Answer
