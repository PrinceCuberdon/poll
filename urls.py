# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#
from django.conf.urls import url

import poll.views

urlpatterns = [
    url(r'^vote/$', poll.views.vote, name='poll_vote'),
    url(r'^results/$', poll.views.results, name="poll_all"),
    url(r'^result/(?P<poll_id>\d+)/$', poll.views.result, name="poll_result")
]
