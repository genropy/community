#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('description')

    def th_order(self):
        return 'description'

    def th_query(self):
        return dict(column='description', op='contains', val='')



class Form(BaseComponent):
    py_requires = 'gnrcomponents/dynamicform/dynamicform:DynamicForm'

    def th_form(self, form):
        bc = form.center.borderContainer()
        top = bc.contentPane(region='top', height='40px', datapath='.record')
        fb = top.formbuilder(cols=2, border_spacing='4px')
        fb.field('description')

        bc.contentPane(region='center').fieldsGrid(margin='2px', rounded=6)


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
