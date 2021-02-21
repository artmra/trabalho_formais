from rest_framework import viewsets
from rest_framework import permissions
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from ine5421 import functions
from django.conf import settings
from .models import FiniteAutomata

from .forms import FiniteAutomataForm, RegularExpressionForm

FILENAME_AF = settings.MEDIA_ROOT+'/af_file'
FILENAME_ER = settings.MEDIA_ROOT+'/er_file'


# testing to import hmtl file as template
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def finite_automata(request):
    form = FiniteAutomataForm()

    context = {
        'form': form,
    }

    return render(request, 'af.html', context)


def regular_expression(request):
    form = RegularExpressionForm()

    context = {
        'form': form,
    }

    return render(request, 'er.html', context)


def upload_af_file(request):
    uploaded_file = request.FILES['afFile']
    # writing file for temp use
    output_file = open(FILENAME_AF, 'w')
    # Check size of file, only open if its not too big
    if not uploaded_file.multiple_chunks():
        file_content = str(uploaded_file.read(), 'utf-8')
        output_file.write(file_content)
    else:
        print('File too big')
    output_file.close()

    # automato = functions.read_af(filename)
    context = {
        'file_content': file_content,
    }

    return render(request, 'af.html', context)


def upload_er_file(request):
    uploaded_file = request.FILES['erFile']
    # writing file for temp use
    output_file = open(FILENAME_AF, 'w')
    # Check size of file, only open if its not too big
    if not uploaded_file.multiple_chunks():
        file_content = str(uploaded_file.read(), 'utf-8')
        output_file.write(file_content)
    else:
        print('File too big')
    output_file.close()

    # automato = functions.read_af(filename)
    context = {
        'file_content': file_content,
    }

    return render(request, 'er.html', context)


def download_af_file(request):
    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=AF.txt'
    return response


def download_er_file(request):
    response = HttpResponse(open(FILENAME_ER, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=ER.txt'
    return response


def update_af_file(request):
    file_content = request.POST['afContent']
    filename = settings.MEDIA_ROOT + '/af_file'
    with open(filename, 'w') as fout:
        print(file_content, file=fout)

    context = {
        'file_content': file_content,
    }

    return render(request, 'af.html', context)


def update_er_file(request):
    file_content = request.POST['erContent']
    filename = settings.MEDIA_ROOT + '/er_file'
    with open(filename, 'w') as fout:
        print(file_content, file=fout)

    context = {
        'file_content': file_content,
    }

    return render(request, 'er.html', context)


def gramatics(request):
    template = loader.get_template('gr.html')
    context = {}
    return HttpResponse(template.render(context, request))


def regex(request):
    template = loader.get_template('er.html')
    context = {}
    return HttpResponse(template.render(context, request))

