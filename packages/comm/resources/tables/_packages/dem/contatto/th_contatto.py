#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('identificativo',width='38em')
        r.fieldcell('email', width='15em')
        r.fieldcell('consenso_id', width='15em')
        r.fieldcell('c_liste', width='20em')
        r.fieldcell('c_argomenti', width='20em')