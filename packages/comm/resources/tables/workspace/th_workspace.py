#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code')
        r.fieldcell('description', width='auto')
        r.fieldcell('developer_id')
        r.fieldcell('link', width='25em')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='')
        

class ViewFromDeveloper(View):
    pass


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
