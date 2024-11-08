# encoding: utf-8
from datetime import datetime
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('organization', pkey='id', name_long='!![en]Organization', name_plural='!![en]Organizations',
                                    caption_field='name',lookup=True)
        self.sysFields(tbl)
        
        tbl.column('code', size=':5', name_long='!![en]Code')
        tbl.column('name', size=':30', name_long='!![en]Name')