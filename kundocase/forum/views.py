from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from kundocase.forum import models, forms


def startpage(request):
    questions = models.Question.objects.all()

    return render(request, 'forum/startpage.html', {
        'questions': questions,
        'form': forms.QuestionForm,
    })


def question(request, id=None):
    """
    Question view handler,
    shows questions and saves new questions

    :param request: Django request object
    :param id: Optional, `Question` object id
    :return: Mixed
    """
    if request.method == 'POST':
        data = dict((k, request.POST.get(k, None)) for k, _ in forms.QuestionForm.base_fields.items())

        form = forms.QuestionForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        try:
            question = models.Question(**data)
            question.save()
            return redirect('forum:question', id=question.id)
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

    question = get_object_or_404(models.Question, id=id)
    answers = question.answer_set.all()

    return render(request, 'forum/question.html', {
        'question': question,
        'answers': answers,
        'form': forms.AnswerForm(initial={'question': question}),
    })


def answer(request, id=None):
    """
    Answer view handler,
    shows answers and saves answers, both new and existing

    :param request: Django request object
    :param id: Optional, `Answer` object id
    :return: Mixed
    """
    if request.method == 'POST':
        data = dict((k, request.POST.get(k, None)) for k, _ in forms.AnswerForm.base_fields.items())
        data['question'] = get_object_or_404(models.Question, id=data.pop('question'))

        try:
            answer, created = models.Answer.objects.update_or_create(id=id, defaults=data)
            if created:
                return redirect('forum:question', id=answer.question.id)
            else:
                return redirect('forum:answer', id=answer.id)

        except ValidationError as e:
            return HttpResponseBadRequest(e.message)

    answer = get_object_or_404(models.Answer, id=id)
    data = {
        'question': answer.question,
        'id': answer.id,
        'content': answer.content,
        'user_name': answer.user_name,
        'user_email': answer.user_email,
    }

    return render(request, 'forum/answer.html', {
        'answer': answer,
        'form': forms.AnswerForm(initial=data),
    })
