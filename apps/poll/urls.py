from django.conf.urls.defaults import *
from models import Space, Query
from forms import QueryForm

urlpatterns = patterns('',
    (r'^$', 'apps.poll.views.index'),
    url(r'^uid/(?P<uid>\w+)/$', 'apps.poll.views.vote', name='vote'),
    url(r'^spaces$', 'apps.poll.views.space_list', name="space-list"),
    url(r'^space/add/$', 'apps.poll.views.space_edit', name="space-add"),
    url(r'^space/edit/(?P<space_id>\d+)/$', 'apps.poll.views.space_edit', name='space-edit'),
    url(r'^space/delete/(?P<space_id>\w+)/$', 'apps.poll.views.space_delete', name="space-delete"),
        
    url(r'^persons$', 'apps.poll.views.person_list', name="person-list"),
    url(r'^persons/add/$', 'apps.poll.views.person_edit', name="person-add"),
    url(r'^persons/edit/(?P<person_id>\w+)/$', 'apps.poll.views.person_edit', name="person-edit"),
    url(r'^persons/delete/(?P<person_id>\w+)/$', 'apps.poll.views.person_delete', name="person-delete"),
    
    url(r'^queries$', 'apps.poll.views.query_list', name="query-list"),
    url(r'^query/add/$', 'apps.poll.views.query_edit', name="query-add"),
    url(r'^query/edit/(?P<query_id>\w+)/$', 'apps.poll.views.query_edit', name="query-edit"),
    url(r'^query/delete/(?P<query_id>\w+)/$', 'apps.poll.views.query_delete', name="query-delete"),
    url(r'^query/view/(?P<query_id>\w+)/$', 'apps.poll.views.query_view', name="query-view"),
    
    url(r'^option/add/(?P<query_id>\w+)/$', 'apps.poll.views.option_edit', name="option-add"),
    url(r'^option/edit/(?P<query_id>\w+)/(?P<option_id>\w+)/$', 'apps.poll.views.option_edit', name="option-edit"),
    url(r'^option/delete/(?P<option_id>\w+)/$', 'apps.poll.views.option_delete', name="option-delete"),
    
    url(r'^poll/list/$', 'apps.poll.views.poll_list', name="poll-list"),
    url(r'^poll/add/(?P<query_id>\w+)/$', 'apps.poll.views.poll_edit', name="poll-add"),

    #(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
