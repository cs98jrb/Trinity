from django.shortcuts import render
from events.models import Event

def index(request):
    latest_question_list = Event.objects.order_by('-pub_date')[:5]
    
    return render(request, 'polls/index.html', {
        'latest_question_list': latest_question_list,
    })