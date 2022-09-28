# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('suggestion_type', pkey='id', caption_field='description', 
                                    name_long='!![en]Suggestion type', name_plural='!![en]Suggestion types')
        self.sysFields(tbl, df=True)

        tbl.column('description', name_long='!![en]Description')
