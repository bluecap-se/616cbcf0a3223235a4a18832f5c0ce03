from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from kundocase.forum import models, forms


def startpage(request):
    questions = models.Question.objects.all()

    return render(request, 'forum/startpage.html', {
        'questions': questions,
        'form': forms.QuestionForm,
    })


def question(request, id):
    question = get_object_or_404(models.Question, id=id)
    answers = question.answer_set.all()

    return render(request, 'forum/question.html', {
        'question': question,
        'answers': answers,
        'form': forms.AnswerForm(initial={'question': question}),
    })


@require_http_methods(['POST'])
def save_question(request):
    data = dict((k, request.POST.get(k, None)) for k, _ in forms.QuestionForm.base_fields.items())

    try:
        question = models.Question(**data)
        question.save()
        return redirect('forum:question', id=question.id)
    except ValidationError as e:
        return HttpResponseBadRequest(e.message)


@require_http_methods(['POST'])
def save_answer(request):
    data = dict((k, request.POST.get(k, None)) for k, _ in forms.AnswerForm.base_fields.items())
    data['question'] = get_object_or_404(models.Question, id=data.pop('question'))

    try:
        answer = models.Answer(**data)
        answer.save()
        return redirect('forum:question', id=answer.question.id)
    except ValidationError as e:
        return HttpResponseBadRequest(e.message)
