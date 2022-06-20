# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('topic', pkey='id', caption_field='description', 
                                    name_long='!![en]Topic', name_plural='!![en]Topics', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_long='!![en]Description')