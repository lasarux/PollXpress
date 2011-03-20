from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.sites.models import Site
from models import Ballot, Poll, Space, Person, Query, Option
from forms import QueryForm, OptionForm, PersonForm, SpaceForm, PollGenerationForm
from datetime import date, datetime

@login_required
def index(request, template='index.html'):
    polls = Poll.objects.filter(date_finish__lte=date.today(), closed=False)
    data = {'polls': polls}
    return render_to_response(template, data, context_instance=RequestContext(request))
    
def space_list(request, template='poll/space.html'):
    spaces = Space.objects.filter(admin=request.user).order_by('name')
    data = {'spaces': spaces}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def space_edit(request, space_id=None, template='poll/space_form.html'):
    """ edit space """
    if space_id:
        instance = Space.objects.get(id=space_id)
        action = _('Edit')
    else:
        instance = None
        action = _('Add')

    if request.method == 'POST':
        form = SpaceForm(request.POST, instance=instance)
        if form.is_valid():
            space = form.save(commit=False)
            space.admin = request.user # check if exist space.admin
            space.save()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully saved space: %s") % space.name)
            return HttpResponseRedirect(reverse('space-list'))
    elif instance:
        form = SpaceForm(instance=instance)
    else:
        form = SpaceForm()
        
    data = {'form': form, 'action':action}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def space_delete(request, space_id, template='poll/space_delete.html'):
    space = Space.objects.get(id=space_id)
    if space.person_set.all():
        raise Http404
    if request.method == 'POST':
        if request.POST.has_key('yes'):
            space.delete()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully deleted space: %s") % space.name)
            return HttpResponseRedirect(reverse('space-list'))
        else:
            return HttpResponseRedirect(reverse('space-list'))

    data = {'space': space}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def person_list(request, template='poll/person.html'):
    spaces = Space.objects.filter(admin=request.user)
    persons = Person.objects.filter(space=None)
    data = {'spaces': spaces, 'persons':persons}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def person_edit(request, person_id=None, template='poll/person_form.html'):
    """ edit person """
    if person_id:
        instance = Person.objects.get(id=person_id)
        action = _('Edit')
    else:
        instance = None
        action = _('Add')

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=instance)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully saved person: %s") % person.name)
            return HttpResponseRedirect(reverse('person-list'))
    elif instance:
        form = PersonForm(instance=instance)
    else:
        form = PersonForm()
        
    data = {'form': form, 'action':action}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def person_delete(request, person_id):
    # TODO: to check if person has open polls
    person = Person.objects.get(id=person_id)
    person.delete()
    messages.add_message(request, messages.SUCCESS,
        ugettext("Successfully deleted person: %s") % person.name)
    return HttpResponseRedirect(reverse('person-list'))

@login_required
def query_list(request, template='poll/query.html'):
    queries = Query.objects.all().order_by('date_creation')
    data = {'queries': queries}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def query_view(request, query_id, template='poll/query_view.html'):
    query = Query.objects.get(id=query_id)
    persons = Person.objects.filter(space__admin=request.user)
    data = {'query': query, 'persons': persons}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def query_delete(request, query_id, template='poll/query_delete.html'):
    query = Query.objects.get(id=query_id)
    if request.method == 'POST':
        if request.POST.has_key('yes'):
            query.option_set.all().delete()
            query.delete()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully deleted query: %s") % query.name)
            return HttpResponseRedirect(reverse('query-list'))
        else:
            return HttpResponseRedirect(reverse('query-list'))

    data = {'query': query}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def query_edit(request, query_id=False, template='poll/query_form.html'):
    if query_id:
        instance = Query.objects.get(id=query_id)
    else:
        instance = None

    if request.method == 'POST':
        form = QueryForm(request.POST, instance=instance)
        if form.is_valid():
            query = form.save(commit=False)
            if not query_id:
                query.user = request.user
            query.save()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully saved query: %s") % query.name)
            return HttpResponseRedirect(reverse('query-view', args=[query.id]))
        
    form = QueryForm(instance=instance)
    data = {'form': form}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def option_edit(request, query_id, option_id=None, template='poll/option_form.html'):
    query = Query.objects.get(id=query_id)
    if option_id:
        instance = Option.objects.get(id=option_id)
    else:
        instance = None

    if request.method == 'POST':
        form = OptionForm(request.POST, instance=instance)
        if form.is_valid():
            option = form.save(commit=False)
            option.query = query
            option.save()
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully saved option: %s") % option.name)
            return HttpResponseRedirect(reverse('query-view', args=[query_id]))
    elif instance:
        form = OptionForm(instance=instance)
    else:
        form = OptionForm()
        
    data = {'form': form}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def option_delete(request, option_id):
    option = Option.objects.get(id=option_id)
    query = option.query
    option.delete()
    messages.add_message(request, messages.SUCCESS,
        ugettext("Successfully deleted option: %s") % option.name)
    return HttpResponseRedirect(reverse('query-view', args=[query.id]))

@login_required
def poll_list(request, template='poll/poll.html'):
    polls = Poll.objects.all().order_by('date_finish')
    data = {'polls': polls}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def poll_edit(request, query_id, template='poll/poll_generation_form.html'):
    query = Query.objects.get(id=query_id)

    if request.method == 'POST':
        form = PollGenerationForm(request.user, request.POST)
        if form.is_valid():
            space = Space.objects.get(id=request.POST['space'])
            query.generate_ballots(space=space, date_finish=form.cleaned_data['date_finish'])
            messages.add_message(request, messages.SUCCESS,
                ugettext("Successfully generated poll: %s") % "test")
            return HttpResponseRedirect(reverse('poll-list'))
    else:
        form = PollGenerationForm(request.user)
        
    data = {'form': form}
    return render_to_response(template, data, context_instance=RequestContext(request))

def vote(request, uid, template='poll/confirm.html'):
    # TODO: show more information when voting is invalid
    try:
        b = Ballot.objects.get(uid=uid)
        r = b.countit()
        if r:
            data = {}
            return render_to_response(template, data, context_instance=RequestContext(request))
        else:
            raise Http404
    except:
        raise Http404
