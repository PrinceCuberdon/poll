# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#
from django.conf.urls import patterns, url

urlpatterns = patterns('poll',
    url(r'^vote/$', 'views.vote', name='poll_vote'),
    url(r'^results/$', 'views.results', name="poll_all"),
    url(r'^result/(?P<poll_id>\d+)/$', 'views.result', name="poll_result")
)
