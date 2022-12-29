# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('lead')
        self.sysFields(tbl)
        
        tbl.column('firstname', name_long='!![en]First name', name_short='!![en]Name')
        tbl.column('lastname', name_long='!![en]Last name', name_short='!![en]Surname')
        tbl.column('message', name_long='!![en]Message')
        tbl.column('privacy', dtype='B', name_long='!![en]Privacy')