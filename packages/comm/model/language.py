# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('language', pkey='code', caption_field='description', 
                                    name_long='!![en]Programming Language', name_plural='!![en]Programming Languages', lookup=True)
        self.sysFields(tbl, id=False)

        tbl.column('code', size=':3', name_long='!![en]Code')
        tbl.column('description', name_long='!![en]Description')
