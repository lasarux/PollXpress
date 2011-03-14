from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from apps.poll.models import Ballot

def index(request, template='index.html'):
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
