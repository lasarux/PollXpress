from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'apps.poll.views.index'),
    (r'^uid/(?P<uid>\w+)/$', 'apps.poll.views.vote'),
    #(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
)
