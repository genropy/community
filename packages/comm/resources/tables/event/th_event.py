#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('title')
        r.fieldcell('event_type_id', hidden=True)
        r.fieldcell('description', width='auto')
        r.fieldcell('event_url', width='25em')
        r.fieldcell('repository_url', width='25em')

    def th_order(self):
        return 'title'

    def th_query(self):
        return dict(column='title', op='contains', val='')

    def th_top_toolbar(self,top):
        top.slotToolbar('*,sections@event_type_id,*', childname='top', _position='<bar')

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
        top = bc.borderContainer(region='top', height='140px', datapath='.record')
        self.eventDetails(top)
        self.eventMeetings(bc.contentPane(region='center'))
        
    def eventDetails(self, top):
        left = top.roundedGroupFrame(region='center', title='!![en]Event details')
        fb = left.formbuilder(cols=2, border_spacing='4px', width='600px')
        fb.field('title')
        fb.field('event_type_id')
        fb.field('description', colspan=2)
        fb.field('event_url', colspan=2)
        fb.field('repository_url', colspan=2)
        self.eventDynamicFields(top.roundedGroupFrame(region='right', width='30%', title='!![en]Additional details'))

    def eventDynamicFields(self, pane):
        pane.dynamicFieldsPane('event_fields')

    def eventMeetings(self, pane):
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', 
                    defaultPrompt=dict(title="!![en]New event",
                                      fields=[dict(value='^.type_id',
                                                    tag='dbSelect',
                                                    lbl='!![en]Event type',
                                                    table='comm.event_type',
                                                    hasDownArrow=True)]))

class FormSupporters(Form):

    def eventMeetings(self, pane):
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True, delrow=False)

class FormDevelopers(FormSupporters):

    def eventDetails(self, pane):
        pane.templateChunk(table='comm.event', record_id='^.id', template='event_info')

    def eventMeetings(self, pane):
        pane.dialogTableHandler(relation='@meetings', 
                                viewResource='ViewFromEvents', pbl_classes=True, addrow=False, delrow=False)

    def th_options(self):
        return dict(readOnly=True)