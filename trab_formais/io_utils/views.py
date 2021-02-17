from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer

from django.template import loader
from django.http import HttpResponse


# just a test view
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# just a test view
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# testing to import hmtl file as template
def index(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': ['a', 'b', 'c'],
    }
    return HttpResponse(template.render(context, request))

def finite_automata(request):
    template = loader.get_template('af.html')
    context = {
        'latest_question_list': ['a', 'b', 'c'],
    }
    return HttpResponse(template.render(context, request))

def gramatics(request):
    template = loader.get_template('gr.html')
    context = {
        'latest_question_list': ['a', 'b', 'c'],
    }
    return HttpResponse(template.render(context, request))

def regex(request):
    template = loader.get_template('er.html')
    context = {
        'latest_question_list': ['a', 'b', 'c'],
    }
    return HttpResponse(template.render(context, request))