#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('username')
        r.fieldcell('fullname')
        r.fieldcell('email')

    def th_order(self):
        return 'fullname'

    def th_query(self):
        return dict(column='fullname', op='contains', val='')

class ViewMap(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('username')
        r.fieldcell('full_address', width='auto')
        r.fieldcell('locality')
        r.fieldcell('country')
        r.fieldcell('position', hidden=True)

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer() 
        top = bc.borderContainer(region='top',height='180px')
        top_left = top.borderContainer(region='center', datapath='.record')
        fb = top_left.contentPane(region='left', width='50%').formbuilder(cols=2,border_spacing='4px',
                            margin='10px')
        fb.field('name')
        fb.field('surname')
        fb.field('email',width='30em',colspan=2)
        fb.geoCoderField(value='^.full_address',colspan=2,
                width='30em',
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
        top_left.contentPane(region='right', padding='10px', width='25%').img(src='^.photo_url',
                crop_height='156px',
                crop_width='156px',
                crop_border='2px dotted silver',
                crop_rounded=6,edit=True,
                placeholder=True,
                upload_folder='site:developers/avatars',
                upload_filename='=#FORM.record.nickname')
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
        tc.contentPane(title='Workspaces').inlineTableHandler(relation='@workspaces', viewResource='ViewFromDeveloper')
        tc.contentPane(title='Projects').inlineTableHandler(relation='@projects', viewResource='ViewFromDeveloper')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')