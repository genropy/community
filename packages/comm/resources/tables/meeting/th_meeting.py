#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('event_id')
        r.fieldcell('title')
        r.fieldcell('start_date', width='10em')
        r.fieldcell('end_date', width='10em')
        r.fieldcell('description', width='auto')
        r.fieldcell('meeting_url', width='25em')

    def th_order(self):
        return 'event_id'

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

class ViewFromEvents(View):

    def th_top_toolbar(self,top):
        pass

class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top', height='110px', datapath='.record').formbuilder(cols=2, 
                                            margin='4px', border_spacing='4px', fld_width='100%')
        fb.field('title', colspan=2)
        fb.field('description', colspan=2)
        fb.field('start_date')
        fb.field('end_date')
        fb.field('meeting_url', colspan=2)

        tc = bc.tabContainer(region='center')
        self.meetingAttachments(tc.contentPane(title='!![en]Attachments'))
        self.meetingDevelopers(tc.contentPane(title='!![en]Developers'))

    def meetingAttachments(self,pane):
        pane.attachmentMultiButtonFrame()

    def meetingDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', picker='developer_id', 
                                viewResource='ViewFromMeetings', pbl_classes=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormSupporters(Form):

    def meetingDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', liveUpdate=True,
                                    viewResource='View', addrow=False, delrow=False)

    def th_top_custom(self, top):
        bar = top.bar.replaceSlots('right_placeholder','subscribe_btn,5,right_placeholder')
        bar.subscribe_btn.slotButton('!![en]Subscribe', 
                    disabled="^#FORM.record.is_developer_subscribed").dataRpc(
                                self.db.table('comm.event_developer').subscribeToevent,
                                        event_id='=#FORM.record.id',
                                        developer_id='=gnr.rootenv.developer_id', 
                                        _onResult='this.form.reload();genro.publish("floating_message",{message:"Subscription successful", messageType:"message"});')

class FormDevelopers(FormSupporters):

    def th_form(self, form):
        bc = form.center.borderContainer()
        bc.contentPane(region='top', height='30%', datapath='.record').templateChunk(table='comm.meeting', 
                                                                                            record_id='^.id',
                                                                                            template='event_info')

        tc = bc.tabContainer(region='center')
        self.meetingAttachments(tc.contentPane(title='!![en]Attachments'))
        self.meetingDevelopers(tc.contentPane(title='!![en]Developers'))

    def th_options(self):
        return dict(readOnly=True)

class FormFromEvents(Form):

    def th_options(self):
        return dict(autoSave=True, showtoolbar=False)