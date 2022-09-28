#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id')
        r.fieldcell('suggestion_id')

    def th_order(self):
        return 'developer_id'

    def th_query(self):
        return dict(column='developer_id', op='contains', val='')

class ViewFromDeveloper(View):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('suggestion_id')
        r.fieldcell('@suggestion_id.description', width='auto')

class ViewFromSuggestions(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id', width='25em', edit=True)
    
    def th_view(self, view):
        bar = view.top.bar.replaceSlots('searchOn','make_initiative,5,searchOn')
        bar.make_initiative.slotButton('!![en]Approve').dataRpc(
                                self.db.table('comm.suggestion_developer').makeInitiativeFromSubscription,
                                                selectedPkeys='=.grid.currentSelectedPkeys')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('developer_id')
        fb.field('suggestion_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
