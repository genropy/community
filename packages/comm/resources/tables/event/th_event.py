#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('event_series_id')
        r.fieldcell('name')
        r.fieldcell('start_date', width='10em')
        r.fieldcell('end_date', width='10em')
        r.fieldcell('event_type_id', hidden=True)
        r.fieldcell('description', width='auto')
        r.fieldcell('event_url', width='25em')

    def th_order(self):
        return 'event_series_id'

    def th_query(self):
        return dict(column='name', op='contains', val='')

    def th_top_toolbar(self,top):
        top.slotToolbar('*,sections@event_type_id,*', childname='top', _position='<bar')

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
        fb = bc.contentPane(region='top', height='30%', datapath='.record').formbuilder(cols=2, border_spacing='4px', fld_width='100%')
        fb.field('name', colspan=2)
        fb.field('description', colspan=2)
        fb.field('start_date')
        fb.field('end_date')
        fb.field('event_url', colspan=2)

        tc = bc.tabContainer(region='center')
        self.eventAttachments(tc.contentPane(title='!![en]Attachments'))
        self.eventDevelopers(tc.contentPane(title='!![en]Developers'))

    def eventAttachments(self,pane):
        pane.attachmentMultiButtonFrame()

    def eventDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', picker='developer_id', viewResource='ViewFromEvents')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormSupporters(Form):

    def eventDevelopers(self, pane):
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
        bc.contentPane(region='top', height='30%', datapath='.record').templateChunk(table='comm.event', 
                                                                                            record_id='^.id',
                                                                                            template='event_info')

        tc = bc.tabContainer(region='center')
        self.eventAttachments(tc.contentPane(title='!![en]Attachments'))
        self.eventDevelopers(tc.contentPane(title='!![en]Developers'))

    def th_options(self):
        return dict(readOnly=True)