from django import forms
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .forms import InputForm, GrammarForm
from json import dumps

import os

from .ine5421.functions import read_af_string, convert_to_gr, union_afs,\
    read_gr_string, read_gr_file, convert_to_af, read_er

FILENAME_AF = settings.MEDIA_ROOT + os.path.sep + 'af_file'
FILENAME_ER = settings.MEDIA_ROOT + os.path.sep + 'er_file'
FILENAME_GR = settings.MEDIA_ROOT + os.path.sep + 'gr_file'


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
    # dependendo de quais opções foram escolhidas no site, chaveia para o método que irá tratá-las de maneira correta
    if request.POST['option'] == 'Ler arquivo':
        return upload_af_file(request)
    elif request.POST['option'] == 'Atualizar AF':
        return update_af_file(request)
    elif request.POST['option'] == 'União':
        return af_union(request)
    elif request.POST['option'] == 'Interseção':
        return af_union(request, inter=True)


def update_af_file(request):
    # tenta atualizar o af; se não houver nada, não atualiza, retorna um erro e tenta mostrar o ultimo AF salvo
    context = dict()
    try:
        file_content = request.POST['file_content']
    except:
        context.update({'error1': 'Não há nada para editar.',
                        'form': InputForm()})
    if 'error1' not in context.keys():
        filename = settings.MEDIA_ROOT + '/af_file'
        try:
            af = read_af_string(file_content)
            with open(filename, 'w') as fout:
                print(file_content, file=fout)
                context.update({'file_content': file_content,
                                'is_afnd': af.is_afnd,
                                'afnodes': dumps(af.get_states_as_vis_nodes()),
                                'afedges': dumps(af.get_transitions_as_vis_edges()),
                                'tried_recognize': False,
                                })
        except Exception as e:
            context.update({'error1': e,
                            'form': InputForm(), })
    return render(request, 'af.html', context)


def upload_af_file(request):
    # tenta construir um af com base no conteúdo do af upado. se não houver tenta mostrar o último af construído
    context = dict()
    try:
        uploaded_file = request.FILES['afFile']
    except:
        context.update({'error1': 'Você não selecionou um arquivo.'})
    if 'error1' not in context.keys():
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
            # lê o af do arquivo
            af = read_af_string(file_content)
            context.update({'afnodes': dumps(af.get_states_as_vis_nodes()),
                            'afedges': dumps(af.get_transitions_as_vis_edges()),
                            'tried_recognize': False,
                            })
        except Exception as e:
            context.update({'error1': e})

    if 'error1' not in context.keys():
        context.update({'is_afnd': af.is_afnd,
                        'file_content': file_content,
                        })
    else:
        if 'file_content' in request.POST.keys():
            af_string = request.POST['file_content']
            try:
                af = read_af_string(af_string)
                # obtém os dados necessários para gerar os grafos aqui
                context.update({'is_afnd': af.is_afnd,
                                'file_content': af_string,
                                'afnodes': dumps(af.get_states_as_vis_nodes()),
                                'afedges': dumps(af.get_transitions_as_vis_edges()),
                                })
            except Exception as e:
                context.update({'error2': e})
                context.update({'file_content': af_string,
                                'form': InputForm()})
        else:
            context.update({'form': InputForm()})
    return render(request, 'af.html', context)


def download_af_file(request):
    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=AF.jff'
    return response


def download_converted_gr(request):
    context = dict()
    if 'file_content' in request.POST.keys():
        af_string = request.POST['file_content']
        try:
            af = read_af_string(af_string)
            converted_gr = convert_to_gr(af)
            converted_gr.write_to_file(FILENAME_GR)
            response = HttpResponse(open(FILENAME_GR, 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=af_to_gr.jff'
            return response
        except Exception as e:
            context.update({'error1': e,
                            'file_content': af_string,
                            'form': InputForm()})
    else:
        context.update({'error1': "Primeiro realize o upload de um arquivo, ou escreva o AF no campo abaixo.",
                        'form': InputForm()})
    return render(request, 'af.html', context)



def determinize(request):
    context = dict()
    try:
        uploaded_file = request.FILES['afFile']
    except:
        context.update({'error1': 'Você não selecionou um arquivo.'})
    if 'error1' not in context.keys():
        # Check size of file, only open if its not too big
        if not uploaded_file.multiple_chunks():
            file_content = str(uploaded_file.read(), 'utf-8')
        else:
            print('File too big')

        try:
            af = read_af_string(file_content)
            af.determinize()
            af.write_to_file(FILENAME_AF)
        except Exception as e:
            context.update({'error1': e})
    else:
        if 'file_content' in request.POST.keys():
            af_string = request.POST['file_content']
            try:
                af = read_af_string(af_string)
                af.determinize()
                af.write_to_file(FILENAME_AF)
            except Exception as e:
                context.update({'error2': e})
                context.update({'file_content': af_string})

    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=af_determinized.jff'
    return response


def minimize(request):
    context = dict()
    try:
        uploaded_file = request.FILES['afFile']
    except:
        context.update({'error1': 'Você não selecionou um arquivo.'})
    if 'error1' not in context.keys():
        # Check size of file, only open if its not too big
        if not uploaded_file.multiple_chunks():
            file_content = str(uploaded_file.read(), 'utf-8')
        else:
            print('File too big')

        try:
            af = read_af_string(file_content)
            af.minimize_af()
            af.write_to_file(FILENAME_AF)
        except Exception as e:
            context.update({'error1': e})
    else:
        if 'file_content' in request.POST.keys():
            af_string = request.POST['file_content']
            try:
                af = read_af_string(af_string)
                af.minimize_af()
                af.write_to_file(FILENAME_AF)
            except Exception as e:
                context.update({'error2': e})
                context.update({'file_content': af_string})

    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=af_minimized.jff'
    return response


def recognize(request):
    context = dict()
    try:
        file_content = request.POST['file_content']
        recognize_content = request.POST['recognize_input']
    except:
        context.update({'error1': 'Você não digitou nada para ser reconhecido.'})
    if 'error1' not in context.keys():
        try:
            af = read_af_string(file_content)
            converted_gr = convert_to_gr(af)
            converted_gr.write_to_file(FILENAME_GR)

            recognized = af.recognize(recognize_content)

            context.update({'is_afnd': af.is_afnd,
                            'afnodes': dumps(af.get_states_as_vis_nodes()),
                            'afedges': dumps(af.get_transitions_as_vis_edges()),
                            'tried_recognize': True,
                            'recognized': recognized
                            })
        except Exception as e:
            context.update({'error1': e})

    if 'error1' not in context.keys():
        context.update({'is_afnd': af.is_afnd,
                        'file_content': file_content,
                        })
    else:
        if 'file_content' in request.POST.keys():
            af_string = request.POST['file_content']
            try:
                af = read_af_string(af_string)

                converted_gr = convert_to_gr(af)
                converted_gr.write_to_file(FILENAME_GR)

                recognized = af.recognize(recognize_content)

                # obtém os dados necessários para gerar os grafos aqui
                context.update({'is_afnd': af.is_afnd,
                                'file_content': af_string,
                                'afnodes': dumps(af.get_states_as_vis_nodes()),
                                'afedges': dumps(af.get_transitions_as_vis_edges()),
                                'tried_recognize': True,
                                'recognized': recognized
                                })
            except Exception as e:
                context.update({'error2': e})
                context.update({'file_content': af_string})
        else:
            context.update({'is_afnd': af.is_afnd,
                            'form': InputForm()
                            })
    return render(request, 'af.html', context)


def af_union(request, inter=False):
    context = dict()
    try:
        uploaded_file = request.FILES['afFile']
    except:
        context.update({'error1': 'Você não selecionou um arquivo.'})
    if 'error1' not in context.keys():
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
            af2 = read_af_string(file_content)
        except Exception as e:
            context.update({'error1': e})

    af1 = read_af_string(request.POST.get('file_content'))

    af_final = union_afs(af1, af2, inter)

    try:
        # obtém os dados necessários para gerar os grafos aqui
        context.update({'file_content': af_final.string_in_file_format(),
                        'afnodes': dumps(af_final.get_states_as_vis_nodes()),
                        'afedges': dumps(af_final.get_transitions_as_vis_edges()),
                        })
    except Exception as e:
        context.update({'error2': e})
        context.update({'file_content': af_final.string_in_file_format()})
    return render(request, 'af.html', context)


#######################################################################################################################
#                                                    GR endpoints                                                     #
#######################################################################################################################

def regular_grammar(request):
    form = GrammarForm()
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
    context = dict()
    form = InputForm()
    try:
        file_content = request.POST['content']
        if file_content == "":
            context.update({'error1': 'Não há nada para editar.',
                            'form': GrammarForm()})
    except:
        context.update({'error1': 'Não há nada para editar.',
                        'form': GrammarForm()})
    if 'error1' not in context.keys():
        filename = settings.MEDIA_ROOT + '/gr_file'
        try:
            gr = read_gr_string(file_content)
            with open(filename, 'w') as fout:
                print(file_content, file=fout)
            customize_gr_form(form, gr, file_content)
            context.update({'form': form})
        except Exception as e:
            context.update({'error1': e})
            context.update({'form': GrammarForm()})
    return render(request, 'gr.html', context)


def upload_gr_file(request):
    context = dict()
    form = InputForm()
    try:
        uploaded_file = request.FILES['grFile']
    except:
        context.update({'error1': 'Você não selecionou um arquivo.'})
    if 'error1' not in context.keys():
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
            gr = read_gr_string(file_content)
        except Exception as e:
            context.update({'error1': e})

    if 'error1' not in context.keys():
        customize_gr_form(form, gr, file_content)
        context.update({'form': form})
    else:
        if 'content' in request.POST.keys():
            gr_string = request.POST['content']
            try:
                gr = read_gr_string(gr_string)
                customize_gr_form(form, gr, gr_string)
                context.update({'form': form})
            except Exception as e:
                context.update({'error2': e})
                context.update({'form': GrammarForm()})
        else:
            context.update({'form': GrammarForm()})
    return render(request, 'gr.html', context)


def customize_gr_form(form, gr, file_content):
    form.fields['content'].initial = file_content
    x = '-1'
    for k in list(gr.productions.keys()):
        x = str(int(x) + 1)
        y = '0'
        form.fields['skip' + x] = forms.BooleanField(widget=forms.HiddenInput())
        form.fields[x + y] = forms.CharField(label=False, required=False, initial=k)
        for v in gr.productions[k]:
            y = str(int(y) + 1)
            form.fields[x + y] = forms.CharField(label=False, required=False, initial=v)


def download_gr_file(request):
    response = HttpResponse(open(FILENAME_GR, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=GR.jff'
    return response


def download_converted_af(request):
    context = dict()
    if 'content' in request.POST.keys():
        gr_string = request.POST['content']
        try:
            gr = read_gr_string(gr_string)
            converted_af = convert_to_af(gr)
            converted_af.write_to_file(FILENAME_AF)
            response = HttpResponse(open(FILENAME_AF, 'rb').read())
            response['Content-Type'] = 'text/plain'
            response['Content-Disposition'] = 'attachment; filename=gr_to_af.jff'
            return response
        except Exception as e:
            form = InputForm()
            customize_gr_form(form, gr, gr_string)
            context.update({'error1': e,
                            'form': form})
    else:
        context.update({'error1': "Primeiro realize o upload de um arquivo, ou escreva a GR no campo abaixo.",
                        'form': GrammarForm()})
    return render(request, 'gr.html', context)


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
    if request.POST['option'] == 'Ler arquivo':
        return upload_er_file(request)
    elif request.POST['option'] == 'Atualizar ER':
        return update_er_file(request)


def update_er_file(request):
    try:
        file_content = request.POST['file_content']
    except:
        context = {'error1': 'Não há nada para editar.',
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
        context = {'error1': 'Você não selecionou um arquivo'}
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

def convertER_to_af(request):
    file_content = request.POST['file_content']
    print(file_content.split(":")[1].strip())
    er = read_er(file_content.split(":")[1].strip())
    converted_af = er.convert_to_af()

    converted_af.write_to_file(FILENAME_AF)
    response = HttpResponse(open(FILENAME_AF, 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=gr_to_af.jff'
    return response

