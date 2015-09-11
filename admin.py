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
from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from libs.poll.models import Poll, Question

#
# class PollAdminForm(forms.ModelForm):
#
#     class Meta:
#         model = Poll
#
#     def clean_name(self):
#         """ Check if there is overlaped polls """
#
#         return self.cleaned_data


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
