#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name')
        r.fieldcell('start_date', width='6em')
        r.fieldcell('end_date', width='6em')
        r.fieldcell('project_type_id', hidden=True)
        r.fieldcell('description', width='auto')
        r.fieldcell('app_url', width='25em')
        r.fieldcell('repository_url', width='25em')
        #r.fieldcell('workspace_id')
        #r.fieldcell('linesofcode', width='6em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

    def th_top_toolbar(self,top):
        top.slotToolbar('*,sections@project_type_id,*', childname='top', _position='<bar')

class ViewDevelopers(View):

    def th_options(self):
        return dict(virtualStore=False, addrow=False, delrow=False)
        
class ViewFromDeveloper(View):

    #def th_view(self, view):
    #    view.top.bar.replaceSlots('delrow','getprojects,2,delrow')
    #    view.top.bar.getprojects.slotButton('!![en]Get projects').dataRpc(
    #            self.db.table('comm.project').getProjects, 
    #                    developer_id='=#FORM.record.id', 
    #                    _ask=dict(title="!![en]Get projects",fields=[dict(
    #                                name="repo_service", lbl="Service", 
    #                                table='sys.service', tag='dbSelect',
    #                                condition='$developer_id=:d_id',
    #                                condition_d_id='=#FORM.record.id',
    #                                hasDownArrow=True,
    #                                auxColumns='$service_type,$implementation,$service_name'),
    #                                dict(name="workspace_slug", lbl="Workspace", 
    #                                table='comm.workspace', tag='dbSelect',
    #                                alternatePkey='code',
    #                                condition='$developer_id=:d_id',
    #                                condition_d_id='=#FORM.record.id',
    #                                hasDownArrow=True)]))

    def th_options(self):
        return dict(searchOn=False)

class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top', height='30%', datapath='.record').formbuilder(cols=2, border_spacing='4px', fld_width='100%')
        fb.field('name', colspan=2)
        fb.field('description', colspan=2)
        fb.field('start_date')
        fb.field('end_date')
        fb.field('app_url', colspan=2)
        fb.field('repository_url', colspan=2)
        #fb.field('workspace_id')
        #fb.div('^.linesofcode_metadata.linesOfCode', lbl='!![en]Lines of code')

        tc = bc.tabContainer(region='center')
        self.projectAttachments(tc.contentPane(title='!![en]Attachments'))
        self.projectDevelopers(tc.contentPane(title='!![en]Developers'))

    def projectAttachments(self,pane):
        pane.attachmentMultiButtonFrame()

    def projectDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', picker='developer_id', 
                                    viewResource='ViewFromProjects', default_status=True)

    #def th_top_custom(self, top):
    #    bar = top.bar.replaceSlots('right_placeholder','countlines,5,right_placeholder')
    #    bar.right_placeholder.slotButton('!![en]Count lines').dataRpc(
    #                            self.db.table('comm.project').countLinesOfCode,
    #                                    reponame='=#FORM.record.name',
    #                                    username='=#FORM.record.project_metadata.owner.login', 
    #                                    project_id='=#FORM.record.id',
    #                                    _ask=dict(title="!![en]Get projects",fields=[dict(
    #                                                name="repo_service", lbl="Service", 
    #                                                table='sys.service', tag='dbSelect',
    #                                                condition="$developer_id=:d_id AND $implementation='git'", #Only available for git projects
    #                                                condition_d_id='=#FORM.record.developer_id',
    #                                                hasDownArrow=True,
    #                                                auxColumns='$service_type,$implementation,$service_name')]))


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormDevelopers(Form):

    def th_form(self, form):
        bc = form.center.borderContainer()
        bc.contentPane(region='top', height='30%', datapath='.record').templateChunk(table='comm.project', 
                                                                                            record_id='^.id',
                                                                                            template='project_info')

        tc = bc.tabContainer(region='center')
        self.projectAttachments(tc.contentPane(title='!![en]Attachments'))
        self.projectDevelopers(tc.contentPane(title='!![en]Developers'))

    def projectDevelopers(self, pane):
        pane.inlineTableHandler(relation='@developers', liveUpdate=True,
                                    viewResource='View', addrow=False, delrow=False)

    def th_top_custom(self, top):
        bar = top.bar.replaceSlots('right_placeholder','subscribe_btn,5,right_placeholder')
        bar.subscribe_btn.slotButton('!![en]Subscribe', 
                    disabled="^#FORM.record.is_developer_subscribed").dataRpc(
                                self.db.table('comm.project_developer').subscribeToProject,
                                        project_id='=#FORM.record.id',
                                        developer_id='=gnr.rootenv.developer_id', 
                                        _onResult='this.form.reload();genro.publish("floating_message",{message:"Request has been sent", messageType:"message"});')

    def th_options(self):
        return dict(readOnly=True)