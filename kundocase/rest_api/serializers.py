import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from kundocase.forum import forms, models


class Serializer:
    form = None
    model = None
    data = []

    def __init__(self, object=None):
        self.object = object
        self.created = False

    def to_representation(self, data):
        data = json.loads(serializers.serialize('json', data))
        self.data = [self.untaint(row) for row in data]

        return self.data

    def to_internal(self, data, *args):
        input_data = json.loads(data) if args[0] else data

        obj = self.model(**input_data)
        obj.save()

        input_data.pop('question')
        self.data = [input_data]
        self.created = True

        return obj

    def untaint(self, row):
        # Converts from {'fields': {'A': 'B'}} to {'A': 'B'}
        original = dict(row.get('fields', {}))

        # Check in `forms` which keys to include or exclude
        data = dict((k, original.get(k, None)) for k, _ in self.form.base_fields.items())

        # Append ID from parent
        data['id'] = row.pop('pk')

        return data

    def response(self):
        status = 200
        if self.created:
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

    def to_internal(self, data, *args):
        input_data = json.loads(data)
        question = get_object_or_404(models.Question, id=args[0])
        input_data['question'] = question

        return super(AnswerSerializer, self).to_internal(input_data, False)
