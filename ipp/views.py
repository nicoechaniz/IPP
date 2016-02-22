from django.shortcuts import render

def portada(request):
    return render(request, 'portada.html', {})

