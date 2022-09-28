#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('approved', semaphore=True)
        r.fieldcell('title')
        r.fieldcell('description')
        r.fieldcell('speakers')
        r.fieldcell('audience')

    def th_order(self):
        return 'title'

    def th_query(self):
        return dict(column='title', op='contains', val='')

    def th_top_toolbar(self,top):
        top.slotToolbar('*,sections@event_type_id,*', childname='top', _position='<bar')

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top', height='30%', datapath='.record').formbuilder(cols=2, border_spacing='4px', fld_width='100%')
        fb.field('title')
        fb.field('description')
        fb.field('speakers')
        fb.field('audience')

        tc = bc.tabContainer(region='center')
        self.suggestionDevelopers(tc.contentPane(title='!![en]Developers'))

    def suggestionDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', picker='developer_id', 
                                            viewResource='ViewFromSuggestions')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormSupporters(Form):

    def suggestionDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', liveUpdate=True,
                                    viewResource='View', addrow=False, delrow=False)

    def th_top_custom(self, top):
        bar = top.bar.replaceSlots('right_placeholder','interested_btn,5,right_placeholder')
        bar.interested_btn.slotButton("!![en]I'm interested", 
                    disabled="^#FORM.record.is_developer_interested").dataRpc(
                                self.db.table('comm.suggestion_developer').interestedInSuggestion,
                                        project_id='=#FORM.record.id',
                                        developer_id='=gnr.rootenv.developer_id', 
                                        _onResult="""this.form.reload();genro.publish("floating_message",
                                                    {message:"You're interested!", messageType:"message"});""")

class FormDevelopers(FormSupporters):

    def th_form(self, form):
        bc = form.center.borderContainer()
        bc.contentPane(region='top', height='30%', datapath='.record').templateChunk(table='comm.project', 
                                                                                            record_id='^.id',
                                                                                            template='project_info')

        tc = bc.tabContainer(region='center')
        self.projectAttachments(tc.contentPane(title='!![en]Attachments'))
        self.projectDevelopers(tc.contentPane(title='!![en]Developers'))
        
    def th_options(self):
        return dict(readOnly=True)