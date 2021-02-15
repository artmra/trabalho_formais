from django.http import HttpResponseForbidden
from django.shortcuts import render


def index(request):
    template_name = 'index.html'

    if request.method == 'POST':
        return HttpResponseForbidden("Method not allowed")

    return render(request, template_name)
