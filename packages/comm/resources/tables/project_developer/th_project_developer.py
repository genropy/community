#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id')
        r.fieldcell('project_id')
        r.fieldcell('role_id')

    def th_order(self):
        return 'developer_id'

    def th_query(self):
        return dict(column='developer_id', op='contains', val='')

class ViewFromDeveloper(View):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('project_id')
        r.fieldcell('role_id')
        r.fieldcell('@project_id.start_date')
        r.fieldcell('@project_id.end_date')
        r.fieldcell('@project_id.description', width='auto')
        r.fieldcell('@project_id.app_url', width='25em')
        r.fieldcell('@project_id.repository_url', width='25em')

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('developer_id')
        fb.field('project_id')
        fb.field('role_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
