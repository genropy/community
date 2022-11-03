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
    py_requires="""gnrcomponents/attachmanager/attachmanager:AttachManager,
                    gnrcomponents/dynamicform/dynamicform:DynamicForm"""

    def th_form(self, form):
        bc = form.center.borderContainer()
        top = bc.borderContainer(region='top', height='120px', datapath='.record')
        self.eventDetails(top.roundedGroupFrame(region='center', title='!![en]Event details'))
        self.eventDynamicFields(top.roundedGroupFrame(region='right', width='30%', title='!![en]Additional details'))
        self.eventMeetings(bc.contentPane(region='center'))
        
    def eventDetails(self, pane):
        fb = pane.formbuilder(cols=3, border_spacing='4px')
        fb.field('name')
        fb.field('description', colspan=2)
        fb.field('event_url', colspan=3)
        fb.field('repository_url', colspan=3)

    def eventDynamicFields(self, pane):
        pane.dynamicFieldsPane('event_fields')

    def eventMeetings(self, pane):
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True)

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
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True, delrow=False)

class FormDevelopers(FormSupporters):

    def eventSeriesEvents(self, pane):
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True, addrow=False, delrow=False)

    def th_options(self):
        return dict(readOnly=True)