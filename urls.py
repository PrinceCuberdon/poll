# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.conf.urls import patterns, url

urlpatterns = patterns('poll',
    url(r'^vote/$', 'views.vote', name='poll_vote'),
    url(r'^results/$', 'views.results', name="poll_all"),
    url(r'^result/(?P<poll_id>\d+)/$', 'views.result', name="poll_result"),
    #url(r'^get_one/$', 'views.get_one', name="poll_get_one"),
)
