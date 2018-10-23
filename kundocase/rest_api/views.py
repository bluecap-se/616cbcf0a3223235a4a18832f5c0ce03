from kundocase.forum import models
from kundocase.rest_api import serializers


def question(request, id=None):
    serializer = serializers.QuestionSerializer()
    data = models.Question.objects

    if id:
        data = data.filter(id=id)

    serializer.to_representation(data.all())

    return serializer.response()


def answer(request, qid, aid=None):
    serializer = serializers.AnswerSerializer()
    data = models.Answer.objects.filter(question__id=qid)

    if aid:
        data = data.filter(id=aid)

    serializer.to_representation(data.all())

    return serializer.response()
