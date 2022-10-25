#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id')
        r.fieldcell('event_id')
        r.fieldcell('role_id')

    def th_order(self):
        return 'developer_id'

    def th_query(self):
        return dict(column='developer_id', op='contains', val='')

class ViewFromDeveloper(View):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('event_id')
        r.fieldcell('role_id')
        r.fieldcell('@meeting_id.start_date')
        r.fieldcell('@meeting_id.end_date')
        r.fieldcell('@meeting_id.description', width='auto')
        r.fieldcell('@meeting_id.event_url', width='25em')

class ViewFromProjects(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id', width='25em', edit=True)
        r.fieldcell('role_id', edit=True)
    
    def th_view(self, view):
        bar = view.top.bar.replaceSlots('searchOn','approve_btn,5,searchOn')
        bar.approve_btn.slotButton('!![en]Approve').dataRpc(
                                self.db.table('comm.project_developer').approveSubscription,
                                                selectedPkeys='=.grid.currentSelectedPkeys')


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('developer_id')
        fb.field('event_id')
        fb.field('role_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
