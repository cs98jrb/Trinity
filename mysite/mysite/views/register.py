from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url

from events.models import Event
from mysite.forms import CreateUserForm


def register(request):

    event_list = Event.objects.filter(
        event_time__gte=timezone.now()
    )[:5]

    redirect_to = request.POST.get('next',
                                   request.GET.get('next', ''))

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url('home page')

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form.save()

            form.login(request)

            return HttpResponseRedirect(redirect_to)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, 'mysite/new_user.html', {
        'form': form,
        'event_list': event_list,
        'redirect_to': redirect_to,
    })