#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method, customizable
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('badge_icon', width='2em', name=' ', 
                            template="<img src='/_rsrc/common/css_icons/svg/16/$badge_icon.svg' width='15px'>")
        r.fieldcell('username', width='16em')
        r.fieldcell('fullname', width='16em')
        r.fieldcell('email', width='16em')
        r.fieldcell('locality', width='6em')
        r.fieldcell('country', width='6em')

    def th_order(self):
        return 'username'

    def th_query(self):
        return dict(column='username', op='contains', val='')

    def th_queryBySample(self):                    
        return dict(fields=[dict(field='$username', lbl='!![en]Username'),
                        dict(field='@languages.language_code', tag='checkboxtext', table='comm.language', 
                                    lbl='!![en]Languages', popup=True, order_by='$description'),
                        dict(field='@topics.topic_id', tag='checkboxtext', table='comm.topic', 
                                    lbl='!![en]Topics', popup=True, order_by='$description'),
                        dict(field='@hobbies.hobby_id', tag='checkboxtext', table='comm.hobby', 
                                    lbl='!![en]Hobbies', popup=True, order_by='$description')
                        ], cols=4, margin='10px', isDefault=True)

class ViewDevelopers(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('username')
        r.fieldcell('locality')
        r.fieldcell('country')
        r.fieldcell('position', hidden=True)
        
    def th_options(self):
        return dict(virtualStore=False, addrow=False, delrow=False)

class ViewMap(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('dev_template', width='auto')
        r.fieldcell('username', hidden=True)
        r.fieldcell('position', hidden=True)
        r.fieldcell('locality', hidden=True)
        r.fieldcell('region', hidden=True)
        r.fieldcell('country', hidden=True)
        r.fieldcell('dev_location', hidden=True)

    def th_queryBySample(self):                    
        pass

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer() 
        top = bc.borderContainer(region='top', height='50%', datapath='.record')
        right = top.borderContainer(region='right', width='300px')
        
        fb = self.developerInfo(top.contentPane(region='left'))
        fb.field('badge_id', hasDownArrow=True)
        
        self.developerUser(right.contentPane(region='bottom', height='100px'))
        self.developerPhoto(right.contentPane(region='center'))
        self.mainContent(bc.tabContainer(region='center',margin='2px'))
    
    @customizable
    def mainContent(self, tc):
        self.developerBio(tc.contentPane(title='!!Bio', datapath='.record', overflow='hidden'))
        self.developerGeoInfo(tc.contentPane(title='!![en]Location', datapath='.record'))
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        self.developerLookupsTab(tc.contentPane(title='!![en]Human Skills'), field='skill')
        self.developerNewsletterTab(tc.borderContainer(title='!![en]Newsletter', checkpref='comm.enable_dem'))
        self.developerProjectsTab(tc.contentPane(title='!![en]Projects'))
        return tc
    
    def developerInfo(self, pane, **kwargs):
        fb = pane.div(padding='5px').mobileFormBuilder(cols=2, border_spacing='8px 0px', **kwargs)
        fb.field('name',validate_notnull=True)
        fb.field('surname',validate_notnull=True)
        fb.field('nickname')
        fb.field('tg_username',lbl='Telegram')
        fb.field('github',colspan=2)
        fb.field('email',colspan=2)
        return fb

    def developerBio(self, pane, **kwargs):
        pane.simpleTextArea('^.bio', height='100%', width='100%', **kwargs)

    def developerGeoInfo(self,pane):
        fb = pane.div(padding='5px').mobileFormBuilder(cols=3, border_spacing='8px 0px')
        fb.geoCoderField(value='^.full_address', lbl='Full address', 
                    selected_locality='.locality',
                    selected_administrative_area_level_1='.region',
                    selected_administrative_area_level_2='.state',
                    selected_administrative_area_level_3='.city',
                    selected_country='.country',
                    selected_position='.position',
                    selectedRecord='.address_bag', 
                    colspan=3)
        fb.field('locality', readOnly=True, hidden='^.full_address?=!#v', colspan=2)
        fb.field('city', readOnly=True, hidden='^.full_address?=!#v')
        fb.field('state', readOnly=True, hidden='^.full_address?=!#v')
        fb.field('region', readOnly=True, hidden='^.full_address?=!#v')
        fb.field('country', readOnly=True, hidden='^.full_address?=!#v')

    def developerPhoto(self, pane):
        pane.img(src='^.photo_url',
                    edit='camera',
                    takePicture=True,
                    crop_margin='auto',
                    crop_margin_top='20px',
                    crop_height='120px',
                    crop_width='120px',
                    crop_border='2px dotted silver',
                    crop_rounded=6,
                    placeholder=True,
                    upload_folder='*')

    def developerUser(self, pane):
        pane.linkerBox('user_id', 
                    addEnabled=True, formResource='Form',
                    default_group_code='COMM',
                    default_firstname='=#FORM.record.name',
                    default_lastname='=#FORM.record.surname',
                    default_email='=#FORM.record.email',
                    dialog_height='500px', dialog_width='800px')   
    
    def developerLookupsTab(self, pane, field=None):
        pane.plainTableHandler(
            table=f'comm.{field}',
            viewResource='ViewRating',
            view_store_onStart=True,
            pbl_classes=True,
            margin='2px',
            searchOn=False,
            configurable=False
        )

    def developerNewsletterTab(self, pane):
        bc = pane.borderContainer()
        bc.contentPane(region='top', height='50px').mobileFormBuilder().radioButtonText(
                        '^.record.consenso', table='dem.consenso_tipo', 
                        lbl='!![en]Level of consent', cols=5, popup=True)
        bc.contentPane(region='center').plainTableHandler(
            table='dem.lista',
            viewResource='ViewSubscription',
            view_store_onStart=True,
            pbl_classes=True,
            margin='2px',
            searchOn=False,
            configurable=False
        )

    def developerProjectsTab(self, pane):
        pane.dialogTableHandler(relation='@projects', pbl_classes=True, 
                                    margin='2px', viewResource='ViewFromDeveloper')

    def developerAccessTab(self, pane):
        fb = pane.contentPane(margin='2px').formbuilder(cols=1)
        fb.lightbutton('!![en]Change password', _class='comm_btn').dataController(
                                                    "genro.mainGenroWindow.genro.publish('openNewPwd')")
        fb.lightbutton('!![en]Delete account', _class='comm_btn').dataRpc(self.db.table('comm.developer').deleteDeveloper, 
                                                    developer_id='=#FORM.pkey', _ask=dict(title="!![en]Are you sure?",
                                                    fields=[dict(name="delete_request", 
                                                            label="!![en]Confirm account deletion", 
                                                            tag='checkbox')]),
                                                    _onResult='genro.logout();')

    @public_method
    def th_onSaving(self,recordCluster,recordClusterAttr=None,resultAttr=None,**kwargs):
        if recordCluster['language_info']:
            self.db.table('comm.developer_language').updateLanguageInfo(developer_id=recordCluster['id'],
                                                        language_info=recordCluster['language_info'])
        if recordCluster['topic_info']:
            self.db.table('comm.developer_topic').updateTopicInfo(developer_id=recordCluster['id'],
                                                        topic_info=recordCluster['topic_info'])
        if recordCluster['hobby_info']:
            self.db.table('comm.developer_hobby').updateHobbyInfo(developer_id=recordCluster['id'],
                                                        hobby_info=recordCluster['hobby_info'])
        if recordCluster['skill_info']:
            self.db.table('comm.developer_skill').updateSkillInfo(developer_id=recordCluster['id'],
                                                        skill_info=recordCluster['skill_info'])
        if recordCluster['newsletter_subscription']:
            self.db.table('dem.contatto_lista').updateNewsletterSubscription(developer_id=recordCluster['id'],
                                                        consenso=recordCluster['consenso'],
                                                        newsletter_subscription=recordCluster['newsletter_subscription'])

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        if newrecord:
            return
        language_info = self.db.table('comm.developer_language').getLanguageInfo(developer_id=record['id'])
        record.addItem('language_info',language_info or Bag(), _sendback=True)
        topic_info = self.db.table('comm.developer_topic').getTopicInfo(developer_id=record['id'])
        record.addItem('topic_info',topic_info or Bag(), _sendback=True)
        hobby_info = self.db.table('comm.developer_hobby').getHobbyInfo(developer_id=record['id'])
        record.addItem('hobby_info',hobby_info or Bag(), _sendback=True)
        skill_info = self.db.table('comm.developer_skill').getSkillInfo(developer_id=record['id'])
        record.addItem('skill_info',skill_info or Bag(), _sendback=True)
        newsletter_subscription = self.db.table('dem.contatto_lista').getNewsletterSubscription(
                                                                        contatto_id=record['contatto_id'])
        record.addItem('newsletter_subscription',newsletter_subscription or Bag(), _sendback=True)
        consenso = self.db.table('dem.contatto').getSubscriptionConsent(contatto_id=record['contatto_id'])
        if consenso:
            record.setItem('consenso', consenso)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class FormDevelopers(Form):

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class FormProfile(Form):
    css_requires='mobile,community'
    
    @customizable
    def th_form(self, form):
        frame = form.center.framePane()
        self.navigationBar(frame.top)
        self.mainContent(frame.center.stackContainer())
        self.saveBar(frame.bottom)

    def navigationBar(self, top):
        top.slotToolbar('*,stackButtons,*', _class='mobile_toolbar', height='38px')
        
    def saveBar(self, bottom):
        bar = bottom.slotToolbar('*,stackButtons,*,savebtn,5', _class='mobile_toolbar', height='38px')
        bar.savebtn.lightButton('!![en]Save', _class='comm_btn', float='right').dataController("this.form.save();")

    def mainContent(self, sc):
        self.profilePage(sc.borderContainer(title='!!Profile', datapath='.record'))
        self.skillsPage(sc.tabContainer(title='!!Skills'))
        self.settingsPage(sc.borderContainer(title='!!Settings'))
    
    def profilePage(self, bc):
        top = bc.contentPane(region='top', height='180px')
        center = bc.borderContainer(region='center')
        self.developerPhoto(top)
        top.div('^#FORM.record.dev_badge', _virtual_column='$dev_badge', _class='dev_badge')
        self.developerInfo(center.contentPane(region='top', height='185px'))
        
        bottom = center.tabContainer(region='center')
        self.developerBio(bottom.contentPane(title='!!Bio', overflow='hidden'))
        self.developerGeoInfo(bottom.contentPane(title='!!Location'))
        
    def skillsPage(self, tc):
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        self.developerLookupsTab(tc.contentPane(title='!![en]Human skills'), field='skill')
        
    def settingsPage(self, bc):
        self.developerNewsletterTab(bc.roundedGroupFrame(title='!![en]Newsletter', region='top', 
                                                         height='200px', checkpref='comm.enable_dem'))
        self.developerAccessTab(bc.roundedGroup(title='!![en]Access', region='center'))
            
    def th_options(self):
        return dict(showtoolbar=False)

class FormMap(Form):
    css_requires='community'
    
    def th_form(self, form):
        bc = form.center.borderContainer(height='100%')
        bc.contentPane(region='center').templateChunk(table='comm.developer', 
                                            record_id='^#FORM.record.id',
                                            template='dev_form')

    def th_options(self):
        return dict(showtoolbar=False)