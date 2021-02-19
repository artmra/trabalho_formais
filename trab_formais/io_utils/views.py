from rest_framework import viewsets
from rest_framework import permissions
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from ine5421 import functions
from django.conf import settings

from .models import FiniteAutomata


# testing to import hmtl file as template
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def finite_automata(request):
    context = {}
    return render(request, 'af.html', context)


def file_upload(request):
    uploaded_file = request.FILES['afFile']
    # writing file for temp use
    filename = settings.MEDIA_ROOT+'/af_file'
    output_file = open(filename, 'w')
    # Check size of file, only open if its not too big
    if not uploaded_file.multiple_chunks():
        output_file.write(str(uploaded_file.read(), 'utf-8'))
    else:
        print('File too big')
    output_file.close()

    automato = functions.read_af(filename)
    context = {
        'file_content': automato,
    }

    FiniteAutomata.objects.create(content=automato)

    return render(request, 'af.html', context)

def gramatics(request):
    template = loader.get_template('gr.html')
    context = {}
    return HttpResponse(template.render(context, request))

def regex(request):
    template = loader.get_template('er.html')
    context = {}
    return HttpResponse(template.render(context, request))

