from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from polls.models import Poll, Choice

#def index(request):
#    latest_polls_list = Poll.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = RequestContext(request, {'latest_polls_list': latest_polls_list})
#    #output = ', '.join([x.question for x in latest_polls_list])
#    return HttpResponse(template.render(context)) # may be as render(request,'polls/index.html', context )
#
#def detail(request, poll_id):
#    # may be one line
#    # poll = get_object_or_404(Poll, pk=poll_id)
#    try:
#        poll = Poll.objects.get(pk=poll_id)
#    except Poll.DoesNotExist:
#        raise Http404
#    return render(request,"polls/detail.html", {'poll': poll}) # (You'relooking at poll %s nigger!" % poll_id)
#
#def results(request, poll_id):
#    poll = get_object_or_404(Poll, pk=poll_id)
#    return render(request, 'polls/results.html', {'poll':poll})

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_polls_list'

    def get_queryset(self):
        """Return last published polls  exclude future"""

        #another way
        #queryset = []
        #for q in Poll.objects.filter(pub_date__lte=timezone.now()):
        #    if q in Poll.objects.filter(choice__gt=0):
        #        queryset.append(q)
        #        if len(queryset)== 5: break

        #super way
        altqueryset = [qu for qu in Poll.objects.filter(pub_date__lte=timezone.now()) if qu in Poll.objects.filter(choice__gt=0)]
        return altqueryset[:5]
            #Poll.objects.filter(pub_date__lte=timezone.now(), choice__gt=0).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_answer = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay voting form
        return render(request, 'polls/detail.html',{
            'poll': p,
            'error_message': "Viberi otvete mazafaka!!00",
        })
    else:
        selected_answer.votes += 1
        selected_answer.save()

        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

