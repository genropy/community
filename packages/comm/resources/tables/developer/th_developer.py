#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('username', width='12em')
        r.fieldcell('fullname', width='12em')
        r.fieldcell('email', width='12em')
        r.fieldcell('locality', width='6em')
        r.fieldcell('country', width='6em')

    def th_order(self):
        return 'fullname'

    def th_query(self):
        return dict(column='fullname', op='contains', val='')

class ViewDevelopers(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('username')
        r.fieldcell('locality')
        r.fieldcell('country')
        r.fieldcell('position', hidden=True)

    def th_page_map(self, pane):
        "Community map"
        map_cp = pane.contentPane(region='center').GoogleMap( 
                        height='100%',
                        map_type='roadmap',
                        centerMarker=True,
                        nodeId='maps',
                        autoFit=True)
        pane.dataController(""" 
                            if(!m.map){
                                        return;
                                    }
                            m.gnr.clearMarkers(m);
                            var that = this;
                            store.forEach(function(n){
                                // console.log(n);
                                m.gnr.setMarker(m, n.attr._pkey, n.attr.position, {title:n.attr.username, 
                                                                                   // labelContent: n.attr.username,
                                                                                   // labelAnchor: new google.maps.Point(15, 0),
                                                                                   // labelClass: "markerlabel" // the CSS class for the label
                                                                                    }
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
        r.fieldcell('username')
        r.fieldcell('locality')
        r.fieldcell('country')
        r.fieldcell('position', hidden=True)

    
class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer() 
        top = bc.borderContainer(region='top',height='180px')
        top_left = top.borderContainer(region='center', datapath='.record')
        fb = top_left.contentPane(region='left', width='600px').formbuilder(cols=2,border_spacing='4px',
                            margin='10px')
        fb.field('name')
        fb.field('surname')
        fb.field('email',width='30em',colspan=2)
        fb.geoCoderField(value='^.full_address', lbl='Full address', 
                colspan=2, width='30em',
                selected_locality='.locality',
                selected_country='.country',
                selected_position='.position')
        fb.field('locality')
        fb.field('country')
        top_left.contentPane(region='center', padding='10px').GoogleMap(
                    height='160px',
                    map_center="^.position",
                    map_type='roadmap',
                    map_zoom=15,
                    centerMarker=True,
                    map_disableDefaultUI=True)
        top_left.contentPane(region='right', padding='10px', width='160px').img(src='^.photo_url',
                crop_height='156px',
                crop_width='156px',
                crop_border='2px dotted silver',
                crop_rounded=6,edit=True,
                placeholder=True,
                upload_folder='site:developers/avatars',
                upload_filename='=#FORM.record.username')
        top_right = top.borderContainer(region='right', width='300px')
        top_right.contentPane(region='top', height='50%', datapath='.record').linkerBox('user_id', 
                                                    addEnabled=True, formResource='Form',
                                                    default_group_code='COMM',
                                                    default_firstname='=#FORM.record.name',
                                                    default_lastname='=#FORM.record.surname',
                                                    default_email='=#FORM.record.email',
                                                    dialog_height='500px', dialog_width='800px')  
        top_right.contentPane(region='center').dialogTableHandler(relation='@services', 
                                                    viewResource='ViewFromDeveloper',
                                                    formResource='FormFromDeveloper',
                                                    default_service_type='repository',
                                                    pbl_classes='*', configurable=False,
                                                    searchOn=False)     

        tc = bc.tabContainer(region='center')
        #tc.contentPane(title='Workspaces').inlineTableHandler(relation='@workspaces', viewResource='ViewFromDeveloper')
        tc.contentPane(title='Projects').dialogTableHandler(
                                                    relation='@projects', viewResource='ViewFromDeveloper',
                                                    addrow=False, delrow=False)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

class FormDevelopers(Form):

    def th_options(self):
        return dict(readOnly=True)