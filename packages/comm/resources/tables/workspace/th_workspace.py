#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description')
        r.fieldcell('developer_id', width='auto')
        r.fieldcell('link', width='auto')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='')

class ViewFromDeveloper(View):

    def th_view(self, view):
        view.top.bar.replaceSlots('delrow','getworkspaces,2,delrow')
        view.top.bar.getworkspaces.slotButton('!![en]Get workspaces').dataRpc(
                self.db.table('comm.workspace').getWorkspaces, 
                        service_name='=#FORM.record.@repo_service.service_name',
                        service_type='=#FORM.record.@repo_service.service_type',
                        developer_id='=#FORM.record.id')

    def th_options(self):
        return dict(searchOn=False)

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('code')
        fb.field('description')
        fb.field('developer_id')
        fb.field('link')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
