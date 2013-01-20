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

from django.conf import settings
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from poll.models import *
from notification import ajax_log
#from jinja2_env import jinja_render_to_response as render_to_response
from django.shortcuts import render_to_response

def vote(request):
    """ Add a vote to the current poll - Ajax way """
    try:
        if request.is_ajax() and request.method == 'POST':
            question = request.POST['question']
            vote = request.POST['vote']
            poll = Poll.objects.get(pk=vote)
            quest = Question.objects.get(pk=question, pool__pk=vote)
            quest.vote += 1
            quest.save()
            if not request.session.has_key('poll_voted'):
                request.session['poll_voted'] = []
            request.session['poll_voted'].append(poll.pk)
            
            return HttpResponse(json.dumps({'results': poll.get_results()}), mimetype = "application/json")
    except Exception as e:
        ajax_log("Poll.vote : %s" % e)
    return HttpResponseBadRequest('OOops - something wrong appends.')
    
def results(request):
    """ Display polls results page """
    try:
        # A poll exists. get the last one 
        return HttpResponseRedirect(reverse('poll_result', args=(Poll.objects.get_latest().pk,)))
    except:
        # No poll. Display the page anyway
        return render_to_response(settings.BANDCOCHON_TEMPLATES.Poll.results, RequestContext(request, {
            'olds' : None,
            'poll' : None,
        }))
        
    
def result(request, poll_id):
    url = reverse('poll_result', args=(poll_id,))
    latests = Poll.objects.get_latests() # Huh ???
    return render_to_response(settings.BANDCOCHON_TEMPLATES.Poll.results, RequestContext(request, {
        'olds': latests,
        'poll': Poll.objects.get(pk=poll_id),
        'url' : url,
        'book_comments': Comment.objects.filter(visible=True, trash=False, url=url, parent=None),        
    }))
  
