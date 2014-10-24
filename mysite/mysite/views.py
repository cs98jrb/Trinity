from django.shortcuts import render

def index(request):
    context = {'x': 'test'}
    return render(request, 'mysite/index.html', context)

def coming_soon(request):
    context = {'title': ''}
    return render(request, 'mysite/coming_soon.html', context)