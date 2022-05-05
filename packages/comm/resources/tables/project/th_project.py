#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name')
        r.fieldcell('description', width='auto')
        r.fieldcell('app_url', width='25em')
        r.fieldcell('repository_url', width='25em')
        r.fieldcell('developer_id')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

class ViewFromDeveloper(View):

    def th_view(self, view):
        view.top.bar.replaceSlots('delrow','getprojects,2,delrow')
        view.top.bar.getprojects.slotButton('!![en]Get projects').dataRpc(
                self.db.table('comm.project').getProjects, 
                        service_name='=#FORM.record.@repo_service.service_name',
                        service_type='=#FORM.record.@repo_service.service_type',
                        developer_id='=#FORM.record.id', 
                        _ask=dict(title="!![en]Get projects",fields=[dict(
                                    name="workspace_slug", lbl="Workspace", 
                                    table='comm.workspace', tag='dbSelect',
                                    alternatePkey='code',
                                    condition='$developer_id=:d_id',
                                    condition_d_id='=#FORM.record.id',
                                    hasDownArrow=True)]))

    def th_options(self):
        return dict(searchOn=False)

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('name')
        fb.field('description')
        fb.field('app_url')
        fb.field('repository_url')
        fb.field('developer_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
