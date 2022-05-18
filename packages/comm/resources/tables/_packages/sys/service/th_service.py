#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import BaseComponent

class ViewFromDeveloper(BaseComponent):
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('implementation', width='auto')

    def th_options(self):
        pass

class FormFromDeveloper(BaseComponent):

    def th_form(self, form):
        form.record.remote(self.buildServiceParameters,service_type='=.service_type',
                                                    implementation='=.implementation',
                                                    service_name='=.service_name', 
                                                    _if="service_type && implementation",
                                                    _fired='^#FORM.controller.loaded',
                                                    _async=True,_waitingMessage=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', modal=True,
                    defaultPrompt=dict(title="!![en]Add a repository service",
                                      fields=[dict(value='^.implementation',
                                                    tag='filteringSelect',
                                                    lbl='!![en]Implementation',
                                                    values="git:Github,bitbucket:Bitbucket",
                                                    hasDownArrow=True)]))

    @public_method
    def buildServiceParameters(self,pane,service_type=None,implementation=None,service_name=None,**kwargs):
        mixinpath = '/'.join(['services',service_type,implementation])
        self.mixinComponent('%s:ServiceParameters' %mixinpath,safeMode=True)
        if hasattr(self,'service_parameters'):
            self.service_parameters(pane,datapath='.parameters', service_name=service_name,
                                    service_type=service_type, implementation=implementation)