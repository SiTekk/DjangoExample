from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from polls.models import Question, Choice


def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now(
    ), id__in=Choice.objects.values_list('question_id').distinct()).order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(render(request, "polls/index.html", context))


def detail(request, question_id):
    try:
        question = Question.objects.filter(
            pub_date__lte=timezone.now(), id__in=Choice.objects.values_list('question_id').distinct()).get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    try:
        question = Question.objects.filter(
            pub_date__lte=timezone.now(), id__in=Choice.objects.values_list('question_id').distinct()).get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    try:
        question = Question.objects.filter(
            pub_date__lte=timezone.now()).get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
