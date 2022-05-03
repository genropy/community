#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import BaseComponent

class FormFromDeveloper(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        fb = bc.contentPane(region='top').formbuilder(cols=2, border_spacing='4px')
        fb.field('service_type',disabled=True)
        fb.field('implementation',disabled=True)
        fb.field('service_name',colspan=2,validate_notnull=True,width='100%',disabled=True)

        center = bc.contentPane(region='center')
        center.contentPane().remote(self.buildServiceParameters,service_type='=.service_type',
                                                    implementation='=.implementation',
                                                    service_name='=.service_name', 
                                                    _if="service_type && implementation",
                                                    _fired='^#FORM.controller.loaded',
                                                    _async=True,_waitingMessage=True)


    @public_method
    def buildServiceParameters(self,pane,service_type=None,implementation=None,service_name=None,**kwargs):
        mixinpath = '/'.join(['services',service_type,implementation])
        self.mixinComponent('%s:ServiceParameters' %mixinpath,safeMode=True)
        if hasattr(self,'service_parameters'):
            self.service_parameters(pane,datapath='.parameters', service_name=service_name,
                                    service_type=service_type, implementation=implementation)