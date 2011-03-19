from django.conf.urls.defaults import *
from models import Space, Query

urlpatterns = patterns('',
    (r'^$', 'apps.poll.views.index'),
    (r'^uid/(?P<uid>\w+)/$', 'apps.poll.views.vote'),
    url(r'^spaces$', 'apps.poll.views.space_list', name="space-list"),
    url(r'^space/add/$', 'django.views.generic.create_update.create_object', {'model' : Space}, name="space-add"),
    url(r'^space/update/(?P<object_id>\d+)/$', 'django.views.generic.create_update.update_object',
        dict(model=Space), name='space-edit'), #, post_save_redirect='/space/%(id)s/')),
    url(r'^persons$', 'apps.poll.views.person_list', name="person-list"),
    url(r'^queries$', 'apps.poll.views.query_list', name="query-list"),
    url(r'^query/add/$', 'django.views.generic.create_update.create_object', {'model' : Query}, name="query-add"),
    url(r'^polls$', 'apps.poll.views.poll_list', name="poll-list"),

    #(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
