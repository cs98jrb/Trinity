from django.shortcuts import render

def index(request):
    context = {'x': 'test'}
    return render(request, 'mysite/base.html', context)
