from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from models import Ballot, Poll, Space
from datetime import date, datetime

def index(request, template='index.html'):
    polls = Poll.objects.filter(date_finish__lte=date.today(), closed=False)
    data = {'polls': polls}
    return render_to_response(template, data, context_instance=RequestContext(request))
    
def space_list(request, template='space.html'):
    spaces = Space.objects.all().order_by('name')
    data = {'spaces': spaces}
    return render_to_response(template, data, context_instance=RequestContext(request))

def space_view(request, space_id=None, template='space.html'):
    data = {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def space_add(request, space_id=None, template='space.html'):
    data = {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def space_edit(request, space_id=None, template='space.html'):
    data = {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def space_remove(request, space_id=None, template='space.html'):
    data = {}
    return render_to_response(template, data, context_instance=RequestContext(request))

def vote(request, uid, template='poll/confirm.html'):
    if len(uid) == 32:
        b = Ballot.objects.get(uid=uid)
        r = b.countit()
        if r:
            data = {}
            return render_to_response(template, data, context_instance=RequestContext(request))
        else:
            raise Http404
    else:
        raise Http404
