from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .forms import InputForm
from ine5421.functions import read_af, read_gr

FILENAME_AF = settings.MEDIA_ROOT + '/af_file'
FILENAME_ER = settings.MEDIA_ROOT + '/er_file'
FILENAME_GR = settings.MEDIA_ROOT + '/gr_file'


# testing to import hmtl file as template
def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


#######################################################################################################################
#                                                    AF endpoints                                                     #
#######################################################################################################################

def finite_automata(request):
    form = InputForm()
    context = {
        'form': form,
    }
    return render(request, 'af.html', context)


def update_or_upload_af(request):
    # talvez não seja a melhor prática, mas por enquanto permite
    if request.POST['option'] == 'Ler arquivo':
        return upload_af_file(request)
    elif request.POST['option'] == 'Atualizar AF':
        return update_af_file(request)


def update_af_file(request):
    try:
        file_content = request.POST['file_content']
    except:
        context = {'error': 'Não há nada para editar.',
                   'form': InputForm(), }
        return render(request, 'af.html', context)
    filename = settings.MEDIA_ROOT + '/af_file'
    with open(filename, 'w') as fout:
        print(file_content, file=fout)
    context = {
        'file_content': file_content,
    }
    return render(request, 'af.html', context)


def upload_af_file(request):
    context = dict()
    try:
        uploaded_file = request.FILES['afFile']
    except:
        context.update({'error': 'Você não selecionou um arquivo.'})
        if 'file_content' in request.POST.keys():
            context.update({'file_content': request.POST['file_content']})
        else:
            context.update({'form': InputForm()})
    if 'error' not in context.keys():
        # writing file for temp use
        output_file = open(FILENAME_AF, 'w')
        # Check size of file, only open if its not too big
        if not uploaded_file.multiple_chunks():
            file_content = str(uploaded_file.read(), 'utf-8')
            output_file.write(file_content)
        else:
            print('File too big')
        output_file.close()

        try:
            af = read_af(FILENAME_AF)
        except Exception as e:
            context.update({'error': e})

    if 'error' not in context.keys():
        context.update({'file_content': file_content})
    else:
        if 'file_content' in request.POST.keys():
            context.update({'file_content': request.POST['file_content']})
        else:
            context.update({'form': InputForm()})
    return render(request, 'af.html', context)


def download_af_file(request):
    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=AF.txt'
    return response


#######################################################################################################################
#                                                    GR endpoints                                                     #
#######################################################################################################################

def regular_grammar(request):
    form = InputForm()
    context = {
        'form': form,
    }
    return render(request, 'gr.html', context)


def update_or_upload_gr(request):
    if request.POST['option'] == 'Ler arquivo':
        return upload_gr_file(request)
    elif request.POST['option'] == 'Atualizar GR':
        return update_gr_file(request)


def update_gr_file(request):
    try:
        file_content = request.POST['file_content']
    except:
        context = {'error': 'Não há nada para editar.',
                   'form': InputForm(), }
        return render(request, 'gr.html', context)
    filename = settings.MEDIA_ROOT + '/gr_file'
    with open(filename, 'w') as fout:
        print(file_content, file=fout)
    context = {
        'file_content': file_content,
    }
    return render(request, 'gr.html', context)


def upload_gr_file(request):
    try:
        uploaded_file = request.FILES['grFile']
    except:
        context = {'error': 'Você não selecionou um arquivo'}
        if 'file_content' in request.POST.keys():
            context.update({'file_content': request.POST['file_content']})
        else:
            context.update({'form': InputForm()})
        return render(request, 'gr.html', context)
    # writing file for temp use
    output_file = open(FILENAME_GR, 'w')
    # Check size of file, only open if its not too big
    if not uploaded_file.multiple_chunks():
        file_content = str(uploaded_file.read(), 'utf-8')
        output_file.write(file_content)
    else:
        print('File too big')
    output_file.close()

    try:
        gr = read_gr(FILENAME_GR)
    except:
        context = {'error': ''}
        
    context = {
        'file_content': file_content,
    }
    return render(request, 'gr.html', context)


def download_gr_file(request):
    response = HttpResponse(open(FILENAME_GR, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=GR.jff'
    return response


#######################################################################################################################
#                                                    ER endpoints                                                     #
#######################################################################################################################


def regular_expression(request):
    form = InputForm()
    context = {
        'form': form,
    }
    return render(request, 'er.html', context)


def update_or_upload_er(request):
    # talvez não seja a melhor prática, mas por enquanto permite
    if request.POST['option'] == 'Ler arquivo':
        return upload_er_file(request)
    elif request.POST['option'] == 'Atualizar ER':
        return update_er_file(request)


def update_er_file(request):
    try:
        file_content = request.POST['file_content']
    except:
        context = {'error': 'Não há nada para editar.',
                   'form': InputForm(), }
        return render(request, 'er.html', context)
    file_content = request.POST['file_content']
    filename = settings.MEDIA_ROOT + '/er_file'
    with open(filename, 'w') as fout:
        print(file_content, file=fout)
    context = {
        'file_content': file_content,
    }
    return render(request, 'er.html', context)


def upload_er_file(request):
    try:
        uploaded_file = request.FILES['erFile']
    except:
        context = {'error': 'Você não selecionou um arquivo'}
        if 'file_content' in request.POST.keys():
            context.update({'file_content': request.POST['file_content']})
        else:
            context.update({'form': InputForm()})
        return render(request, 'er.html', context)
    # writing file for temp use
    output_file = open(FILENAME_ER, 'w')
    # Check size of file, only open if its not too big
    if not uploaded_file.multiple_chunks():
        file_content = str(uploaded_file.read(), 'utf-8')
        output_file.write(file_content)
    else:
        print('File too big')
    output_file.close()
    # implementação de ER necessária
    context = {
        'file_content': file_content,
    }
    return render(request, 'er.html', context)


def regex(request):
    template = loader.get_template('er.html')
    context = {}
    return HttpResponse(template.render(context, request))


def download_er_file(request):
    response = HttpResponse(open(FILENAME_ER, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=ER.jff'
    return response
