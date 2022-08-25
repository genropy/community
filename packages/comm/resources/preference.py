#!/usr/bin/env python
# encoding: utf-8

class AppPref(object):

    def permission_comm(self,**kwargs):
        return 'admin'

    def prefpane_comm(self,parent,**kwargs): 
        pane = parent.contentPane(**kwargs)
        fb = pane.formbuilder(cols=1,border_spacing='3px', margin='10px')
        fb.dbSelect(value='^.default_srvy', table='srvy.survey', lbl='!![it]Survey default')
        fb.dbSelect(value='^.user_default_badge', table='comm.badge', lbl='!![it]New user default badge')