# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>
#

import logging

from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse

from poll.models import *
from django.shortcuts import render_to_response
from ucomment.models import Comment

L = logging.getLogger("poll")


def vote(request):
    """ Add a vote to the current poll - Ajax way """
    try:
        if request.is_ajax() and request.method == 'POST':
            question = request.POST['question']
            v = request.POST['vote']
            poll = Poll.objects.get(pk=v)
            quest = Question.objects.get(pk=question, pool__pk=v)
            quest.vote += 1
            quest.save()
            if not request.session.has_key('poll_voted'):
                request.session['poll_voted'] = []
            request.session['poll_voted'].append(poll.pk)

            return JsonResponse({'results': poll.get_results()})
    except Exception as e:
        L.error(u"poll.views.vote : {error}".format(error=e))

    return HttpResponseBadRequest('OOops - something wrong appends.')


def results(request):
    """ Display polls results page """
    try:
        # A poll exists. get the last one 
        return HttpResponseRedirect(reverse('poll_result', args=(Poll.objects.get_latest().pk,)))
    except Exception as e:
        # No poll. Display the page anyway
        L.error(u"poll.views.results: Unable to display results. Reasons : {error}".format(error=e))
        return render_to_response(settings.BANDCOCHON_TEMPLATES.Poll.results, RequestContext(request, {
            'olds': None,
            'poll': None,
        }))


def result(request, poll_id):
    url = reverse('poll_result', args=(poll_id,))
    latests = Poll.objects.get_latests()  # Huh ???
    return render_to_response(settings.BANDCOCHON_TEMPLATES.Poll.results, RequestContext(request, {
        'olds': latests,
        'poll': Poll.objects.get(pk=poll_id),
        'url': url,
        'book_comments': Comment.objects.filter(visible=True, trash=False, url=url, parent=None),
    }))
