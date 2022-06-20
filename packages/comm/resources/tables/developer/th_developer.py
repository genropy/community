#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tg_username', width='12em')
        r.fieldcell('fullname', width='12em')
        r.fieldcell('email', width='12em')
        r.fieldcell('locality', width='6em')
        r.fieldcell('country', width='6em')

    def th_order(self):
        return 'fullname'

    def th_query(self):
        return dict(column='fullname', op='contains', val='')

    def th_queryBySample(self):                    
        return dict(fields=[dict(field='$tg_username', lbl='!![en]Tg username'),
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
        r.fieldcell('tg_username')
        r.fieldcell('locality')
        r.fieldcell('country')
        r.fieldcell('position', hidden=True)
        
    def th_page_map(self, pane):
        "Community map"
        map_cp = pane.GoogleMap( 
                        height='100%',
                        map_type='roadmap',
                        centerMarker=True,
                        nodeId='dev_maps',
                        autoFit=True)
        pane.dataController(""" 
                            if(!m.map){
                                        return;
                                    }
                            m.gnr.clearMarkers(m);
                            var that = this;
                            store.forEach(function(n){
                                console.log(n);
                                m.gnr.setMarker(m, n.attr._pkey, n.attr.position, {title:n.attr.tg_username}
                                                );
                            }, 'static');
                         """,
                            m=map_cp,
                            store='^.store',
                            _delay=100)

    def th_options(self):
        return dict(virtualStore=False, addrow=False, delrow=False)

class ViewMap(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('dev_template', width='auto')
        r.fieldcell('tg_username', hidden=True)
        r.fieldcell('position', hidden=True)

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
        self.developerServices(right.contentPane(region='center', datapath='#FORM'))

        tc= bc.tabContainer(region='center',margin='2px')
        self.developerGeoInfo(tc.contentPane(title='Address', datapath='.record').div(
                    padding='20px',padding_right='40px'))
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        self.developerProjectsTab(tc.contentPane(title='!![en]Projects'))

    def developerInfo(self, pane):
        fb = pane.div(padding='20px', padding_right='40px').formbuilder(cols=1, width='100%',
                    colswidth='auto', fld_width='100%', border_spacing='6px')
        fb.field('name')
        fb.field('surname')
        fb.field('email')
        fb.field('tg_username')
        fb.field('nickname')
        fb.field('github')
        fb.field('website')
        fb.field('bio', tag='simpleTextArea', height='100px')
    
    def developerGeoInfo(self,pane):
        fb = pane.formbuilder(cols=1, width='100%', colswidth='auto',
                    fld_width='100%', border_spacing='6px')
        fb.geoCoderField(value='^.full_address', lbl='Full address', 
                    selected_locality='.locality',
                    selected_administrative_area_level_1='.region',
                    selected_administrative_area_level_2='.state',
                    selected_administrative_area_level_3='.city',
                    selected_country='.country',
                    selected_position='.position')
        fb.field('locality')
        fb.field('city')
        fb.field('state')
        fb.field('region')
        fb.field('country')

    def developerPhoto(self, pane):
        pane.img(src='^.photo_url',
                    edit='camera',
                    crop_margin='auto',
                    crop_margin_top='20px',
                    crop_height='170px',
                    crop_width='170px',
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

    def developerServices(self, pane):
        pane.dialogTableHandler(relation='@services', 
                                    viewResource='ViewFromDeveloper',
                                    formResource='FormFromDeveloper',
                                    default_service_type='repository',
                                    pbl_classes='*', configurable=False,
                                    searchOn=False)     
    
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

    def developerProjectsTab(self, pane):
        pane.dialogTableHandler(relation='@projects', pbl_classes=True, 
                                    margin='2px',viewResource='ViewFromDeveloper')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormDevelopers(Form):

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormProfile(Form):
    css_requires='community'

    def th_form(self, form):
        bc = form.center.borderContainer() 
        top = bc.contentPane(region='top',height='60px', datapath='.record')
        top.h1('^.tg_username', _class='dev_username')
        tc = bc.tabContainer(region='center',margin='2px', _class='profile_center')
        dev_info = tc.borderContainer(title='!![en]Developer info',datapath='.record')
        self.developerPhoto(dev_info.contentPane(region='top'))
        self.developerInfo(dev_info.contentPane(region='center'))
        self.developerGeoInfo(tc.contentPane(title='!![en]Address', datapath='.record').div(padding='20px',padding_right='40px'))
        self.developerLookupsTab(tc.contentPane(title='!![en]Languages'), field='language')
        self.developerLookupsTab(tc.contentPane(title='!![en]Topics'), field='topic')
        self.developerLookupsTab(tc.contentPane(title='!![en]Hobbies'), field='hobby')
        bc.contentPane(region='bottom', height='50px').lightbutton(
                '!![en]Save', _class='comm_btn').dataController("this.form.save();")

    @public_method
    def th_onSaving(self,recordCluster,recordClusterAttr=None,resultAttr=None,**kwargs):
        self.db.table('comm.developer_language').updateLanguageInfo(developer_id=recordCluster['id'],
                                                        language_info=recordCluster['language_info'])
        self.db.table('comm.developer_topic').updateTopicInfo(developer_id=recordCluster['id'],
                                                        topic_info=recordCluster['topic_info'])
        self.db.table('comm.developer_hobby').updateHobbyInfo(developer_id=recordCluster['id'],
                                                        hobby_info=recordCluster['hobby_info'])

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        if newrecord:
            return
        language_info = self.db.table('comm.developer_language').getLanguageInfo(
                                                        developer_id=record['id'])
        record.addItem('language_info',language_info or Bag(), _sendback=True)
        topic_info = self.db.table('comm.developer_topic').getTopicInfo(
                                                        developer_id=record['id'])
        record.addItem('topic_info',topic_info or Bag(), _sendback=True)
        hobby_info = self.db.table('comm.developer_hobby').getHobbyInfo(
                                                        developer_id=record['id'])
        record.addItem('hobby_info',hobby_info or Bag(), _sendback=True)

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