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
    py_requires="gnrcomponents/dynamicform/dynamicform:DynamicForm"

    def th_form(self, form):
        bc = form.center.borderContainer()
        top = bc.borderContainer(region='top', height='200px', datapath='.record')
        tc = bc.tabContainer(region='center')
        self.suggestionDetails(top)
        self.suggestionDevelopers(tc.contentPane(title='!![en]Developers'))

    def suggestionDetails(self, top):
        left = top.roundedGroupFrame(region='center', title='!![en]Suggestion details')
        fb = left.formbuilder(cols=2, border_spacing='4px', fld_width='100%')
        fb.field('title')
        fb.field('suggestion_type_id', readOnly=True)
        fb.field('developer_id', readOnly=True)
        fb.checkboxtext('^.topics', table='comm.topic', lbl='!![en]Topics', popup=True)
        fb.field('description', colspan=2)
        fb.field('speakers', colspan=2)
        fb.field('audience', colspan=2)
    
        self.suggestionDynamicFields(top.roundedGroupFrame(region='right', width='30%', title='!![en]Additional details'))

    def suggestionDynamicFields(self, pane):
        pane.dynamicFieldsPane('suggestion_fields')

    def suggestionDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', picker='developer_id', 
                                            viewResource='ViewFromSuggestions', pbl_classes=True)

    def th_top_bar(self, top):
        bar = top.bar.replaceSlots('right_placeholder','right_placeholder,5,make_initiative')
        bar.make_initiative.slotButton('!![en]Make initiative').dataRpc(
                                self.db.table('comm.suggestion').makeInitiativeFromSuggestion,
                                            record='=#FORM.record',
                                            _ask=dict(title="!![en]Make initiative from suggestion",
                                                    fields=[dict(name="initiative_type", 
                                                            lbl="!![en]Initiative type", 
                                                            tag='filteringSelect',
                                                            values='project:!![en]Project,event:!![en]Event,meeting:!![en]Meeting')]))

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', 
                    defaultPrompt=dict(title="!![en]New suggestion",
                                      fields=[dict(value='^.suggestion_type_id',
                                                    tag='dbSelect',
                                                    lbl='!![en]Suggestion type',
                                                    table='comm.suggestion_type',
                                                    hasDownArrow=True)]))

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

    #def suggestionDetails(self, pane):
    #    pane.templateChunk(table='comm.suggestion', record_id='^.id', template='suggestion_info')
        
    def th_options(self):
        return dict(readOnly=True)