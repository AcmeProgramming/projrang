from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse



def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "Content from context_dict in index def apprang.views"}
    return render_to_response('apprang/index.html', context_dict, context)

def about(request):
    about_context = RequestContext(request)
    about_context_dict = {'boldmessage': "This is bold messaging information from about def"}
    return render_to_response('apprang/about.html', about_context_dict, about_context)
