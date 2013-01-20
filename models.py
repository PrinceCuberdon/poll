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

import datetime
import json

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ucomment.models import Comment

class PollManager(models.Manager):
    def get_current(self):
        """ Get the current active poll """
        now = datetime.date.today()
        try:
            return Poll.objects.get(start_date__lte=now, end_date__gte=now)
        except:
            return None

    def get_latests(self):
        """ Return lasted except current """
        return Poll.objects.filter(end_date__lt=datetime.date.today())
    
    def get_latest(self):
        """ Get the latest poll regarding publication date """
        now = datetime.date.today()
        try:
            return Poll.objects.filter(end_date__lte=now)[0]
        except:
            pass
        return []
    
class Poll(models.Model):
    question = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    
    objects = PollManager()
    
    def __unicode__(self):
        return self.question
    
    def admin_get_question_count(self):
        return Question.objects.filter(pool=self).count()
    admin_get_question_count.short_description = "Nombre de questions"
    admin_get_question_count.admin_order_field = "question"
    
    def get_vote_count(self):
        total = 0
        for q in Question.objects.filter(pool=self):
            total += q.vote
        return total
    get_vote_count.short_description = "Nombre de votants"
    get_vote_count.admin_order_field = "question__vote"
    
    def get_related_questions(self):
        """ Return all Question for this poll """
        return Question.objects.filter(pool=self)
        
    def get_absolute_url(self):
        return reverse('poll_result', args=(self.pk, ))
        
    def get_results(self):
        """ Return poll result for json transaction """
        results = []
        count = 0
        for p in Question.objects.filter(pool=self):
            results.append({'label':p.label, 'vote':p.vote })
            count += p.vote
        
        for i in range(len(results)):
            results[i]['vote'] = round(float(results[i]['vote']) / float(count) * 100.0, 2)
            
        return results
    
class Question(models.Model):
    pool = models.ForeignKey('Poll', related_name="poll") # Sorry for the typing error
    label = models.CharField(max_length=100)
    vote = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.label
    
    def admin_get_votes(self):
        return self.vote
    admin_get_votes.short_description = "Votes"
    admin_get_votes.admin_order_field = 'vote'
    
    def admin_get_percent(self):
        return "%2.f %%" % self.get_percent()
    admin_get_percent.short_description = "Pourcentage"
    
    def get_size(self):
        """ """
        try:
            allquestions = self.pool.get_vote_count()
            return int(float(self.vote) / allquestions * 160) # 160 is the size in pixels FIXME!!!!
        except:
            return 0
        
    def get_percent(self):
        """ """
        try:
            allquestions = self.pool.get_vote_count()
            return int(float(self.vote) / allquestions * 100)
        except:
            return 0
      
