# -*- coding: UTF-8 -*-
# poll is part of Band Cochon
# Band Cochon (c) Prince Cuberdon 2011 and Later <princecuberdon@bandcochon.fr>

from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from poll.models import Poll, Question


class RequiredInlineFormSet(BaseInlineFormSet):
    """ Found on Stackoverflow """

    def _construct_form(self, i, **kwargs):
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    formset = RequiredInlineFormSet


class PollAdmin(admin.ModelAdmin):
    # form = PollAdminForm
    list_display = ('__unicode__', 'start_date', 'end_date', 'admin_get_question_count', 'get_vote_count',)
    date_hierarchy = "end_date"
    inlines = [QuestionInline, ]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'pool', 'admin_get_votes', 'admin_get_percent',)
    list_filter = ('pool',)


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
