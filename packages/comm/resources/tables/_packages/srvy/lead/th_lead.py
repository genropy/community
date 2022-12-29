#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('email')
        r.fieldcell('firstname')
        r.fieldcell('lastname')
        r.fieldcell('message')
        r.fieldcell('privacy')

    def th_order(self):
        return 'email'

    def th_query(self):
        return dict(column='email', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('email')
        fb.field('firstname')
        fb.field('lastname')
        fb.field('message', tag='simpleTextArea', width='100%', height='50px', colspan=2)
        fb.field('privacy')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')