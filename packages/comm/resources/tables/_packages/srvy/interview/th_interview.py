#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('developer_id')
        r.fieldcell('survey_id')
        r.fieldcell('start_ts',width='12em')
        r.fieldcell('end_ts',width='12em')
        r.fieldcell('perc_answers',format='progress',cellClasses='progressCell',name='Status')
        r.fieldcell('link',width='30em',name='Link', template="<a href='$link' target='_blank'>$link</a>")