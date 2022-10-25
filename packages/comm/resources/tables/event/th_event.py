#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name')
        r.fieldcell('type_id', hidden=True)
        r.fieldcell('description', width='auto')
        r.fieldcell('event_url', width='25em')
        r.fieldcell('repository_url', width='25em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

    def th_top_toolbar(self,top):
        top.slotToolbar('*,sections@type_id,*', childname='top', _position='<bar')

class ViewDevelopers(View):

    def th_options(self):
        return dict(virtualStore=False, addrow=False, delrow=False)

class ViewSupporters(View):

    def th_options(self):
        return dict(virtualStore=False, delrow=False)

class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top', datapath='.record').formbuilder(cols=3, border_spacing='4px', fld_width='100%')
        fb.field('name')
        fb.field('description', colspan=2)
        fb.field('event_url', colspan=3)
        fb.field('repository_url', colspan=3)

        self.eventsSeries(bc.roundedGroupFrame(region='center', title='!![en]Events', pbl_classes='*'))

    def eventsSeries(self, pane):
        pane.borderTableHandler(relation='@meetings', formResource='FormFromEvents',
                                                                            viewResource='ViewFromEvents')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', 
                    defaultPrompt=dict(title="!![en]Event type",
                                      fields=[dict(value='^.type_id',
                                                    tag='dbSelect',
                                                    lbl='!![en]Event type',
                                                    table='comm.event_type',
                                                    hasDownArrow=True)]))

class FormSupporters(Form):

    def eventSeriesEvents(self, pane):
        pane.borderTableHandler(relation='@meetings', viewResource='ViewSupporters', vpane_height='30%',
                                    formResource='FormSupporters', delrow=False)

class FormDevelopers(FormSupporters):

    def eventSeriesEvents(self, pane):
        pane.borderTableHandler(relation='@meetings', viewResource='ViewDevelopers', vpane_height='30%',
                                    formResource='FormDevelopers', addrow=False, delrow=False)

    def th_options(self):
        return dict(readOnly=True)