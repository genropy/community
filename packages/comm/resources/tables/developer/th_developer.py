#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method, customizable
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('badge_icon', width='2em', name=' ', 
                            template="<img src='/_rsrc/common/css_icons/svg/16/$badge_icon.svg' width='15px'")
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
        top = bc.borderContainer(region='top',height='50%', datapath='.record')
        self.developerInfo(top.contentPane(region='left', width='600px'))
        self.developerPhoto(top.contentPane(region='center'))
        right = top.borderContainer(region='right', width='300px')
        self.developerUser(right.contentPane(region='top', height='100px'))
        self.developerBadge(right.roundedGroupFrame(region='center', title='!![en]Badge', height='60px'))

        tc=bc.tabContainer(region='center',margin='2px')
        self.mainContent(tc)
    
    @customizable
    def mainContent(self, tc):
       #self.developerGeoInfo(tc.contentPane(title='Address', datapath='.record').div(
       #            padding='20px',padding_right='40px'))
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        self.developerLookupsTab(tc.contentPane(title='!![en]Skills'), field='skill')
        self.developerNewsletterTab(tc.contentPane(title='!![en]Newsletter', checkpref='comm.enable_dem'))
        self.developerProjectsTab(tc.contentPane(title='!![en]Projects'))
        return tc
    
    def developerInfo(self, pane, **kwargs):
        fb = pane.div(padding='10px').formbuilder(cols=3, border_spacing='8px 0px', 
                        width='100%',fld_width='100%',**kwargs)
        fb.field('name',validate_notnull=True)
        fb.div(width='10px')
        fb.field('surname',validate_notnull=True)
        fb.field('full_address', lbl='!![en]Full address', tag='geocoderfield',
                    selected_locality='.locality',
                    selected_administrative_area_level_1='.region',
                    selected_administrative_area_level_2='.state',
                    selected_administrative_area_level_3='.city',
                    selected_country='.country',
                    selected_position='.position',
                    selectedRecord='.address_bag')
        fb.div(width='10px')            
        fb.field('position',protected=True)
        fb.field('nickname')
        fb.div(width='10px')
        fb.field('tg_username',lbl='Telegram')
        fb.field('github',colspan=3)
        fb.field('email',colspan=3)
        fb.field('website',colspan=3)
        fb.field('bio', tag='simpleTextArea', height='80px',colspan=3)

    #def developerGeoInfo(self,pane):
    #    fb = pane.formbuilder(cols=1, width='100%', colswidth='auto',
    #                fld_width='100%', border_spacing='6px')
    #    fb.geoCoderField(value='^.full_address', lbl='Full address', 
    #                selected_locality='.locality',
    #                selected_administrative_area_level_1='.region',
    #                selected_administrative_area_level_2='.state',
    #                selected_administrative_area_level_3='.city',
    #                selected_country='.country',
    #                selected_position='.position',
    #                selectedRecord='.address_bag')
    #    fb.field('locality', readOnly=True, hidden='^.full_address?=!#v')
    #    fb.field('city', readOnly=True, hidden='^.full_address?=!#v')
    #    fb.field('state', readOnly=True, hidden='^.full_address?=!#v')
    #    fb.field('region', readOnly=True, hidden='^.full_address?=!#v')
    #    fb.field('country', readOnly=True, hidden='^.full_address?=!#v')

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

    def developerBadge(self, pane):
        fb = pane.formbuilder(cols=1, width='100%', fld_width='90%')
        fb.dbSelect('^.badge_id', table='comm.badge', hasDownArrow=True)

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
        bc.contentPane(region='top', height='30px').formbuilder().radioButtonText(
                        '^.record.consenso', table='dem.consenso_tipo', 
                        lbl='!![en]Level of consent', cols=5)
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
    css_requires='community'

    @customizable
    def th_form(self, form):
        bc = form.center.borderContainer() 
        tc = bc.tabContainer(region='center',margin='2px', _class='profile_center')
        dev_info = tc.borderContainer(title='!![en]Developer info',datapath='.record')
        self.developerPhoto(dev_info.contentPane(region='top'))
        self.developerInfo(dev_info.contentPane(region='center'), 
                        lblpos='T',
                        lbl_text_align='left',lbl_font_size='.8em',
                        lbl_padding_top='4px',
                        lbl_font_weight='bold',fldalign='left',
                        _class='mobilefields')
        #self.developerGeoInfo(tc.contentPane(title='!![en]Address', datapath='.record').div(padding='20px',padding_right='40px'))
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        self.developerLookupsTab(tc.contentPane(title='!![en]Skills'), field='skill')
        self.developerNewsletterTab(tc.contentPane(title='!![en]Newsletter', checkpref='comm.enable_dem'))
        self.developerAccessTab(tc.contentPane(title='!![en]Access'))
        bc.contentPane(region='bottom', height='50px').lightbutton(
                        '!![en]Save', _class='comm_btn', float='right').dataController("this.form.save();")
        return tc
    
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