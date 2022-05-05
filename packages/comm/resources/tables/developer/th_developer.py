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

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer() 
        top = bc.borderContainer(region='top',datapath='.record',height='180px')
        fb = top.contentPane(region='left').formbuilder(cols=2,border_spacing='4px',
                            margin='10px')
        fb.field('name')
        fb.field('surname')
        fb.field('email',width='30em',colspan=2)
        fb.field('full_address',colspan=2,
                width='30em',
                selected_locality='.locality',
                selected_country='.country',
                selected_position='.position',
                tag='geoCoderField')
        fb.field('locality')
        fb.field('country')
        top.contentPane(region='center',padding='10px').img(src='^.photo_url',
                crop_height='150px',
                crop_width='150px',
                crop_border='2px dotted silver',
                crop_rounded=6,edit=True,
                placeholder=True,
                upload_folder='site:developers/avatars',
                upload_filename='=#FORM.record.nickname')
        top_right = top.borderContainer(region='right', width='300px')
        top_right.contentPane(region='top', height='50%').linkerBox('user_id', 
                                                    addEnabled=True, formResource='Form',
                                                    default_group_code='COMM',
                                                    default_firstname='=#FORM.record.name',
                                                    default_lastname='=#FORM.record.surname',
                                                    default_email='=#FORM.record.email',
                                                    dialog_height='500px', dialog_width='800px')  
        top_right.contentPane(region='center').linkerBox('repo_service', 
                                                    addEnabled=True, formResource='FormFromDeveloper',
                                                    default_service_name='=#FORM.record.@user_id.username',
                                                    default_implementation='bitbucket',
                                                    default_service_type='bitbucket',
                                                    dialog_height='500px', dialog_width='800px')     

        tc = bc.tabContainer(region='center')
        tc.contentPane(title='Workspaces').inlineTableHandler(relation='@workspaces', viewResource='ViewFromDeveloper')
        tc.contentPane(title='Projects').inlineTableHandler(relation='@projects', viewResource='ViewFromDeveloper')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')