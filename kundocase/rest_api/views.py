from django.views.decorators.csrf import csrf_exempt
from kundocase.forum import models
from kundocase.rest_api import serializers


@csrf_exempt
def question(request, id=None):
    serializer = serializers.QuestionSerializer()
    data = models.Question.objects

    if request.method == 'POST':
        serializer.to_internal(request.body)
    else:
        if id:
            data = data.filter(id=id)

        serializer.to_representation(data.all())

    return serializer.response()


@csrf_exempt
def answer(request, qid, aid=None):
    serializer = serializers.AnswerSerializer()
    data = models.Answer.objects.filter(question__id=qid)

    if request.method == 'POST':
        serializer.to_internal(request.body, qid)
    else:
        if aid:
            data = data.filter(id=aid)

        serializer.to_representation(data.all())

    return serializer.response()
