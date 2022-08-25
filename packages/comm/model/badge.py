# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('badge', pkey='id', caption_field='description', 
                                    name_long='!![en]Badge', name_plural='!![en]Badges', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_long='!![en]Description')
        tbl.column('icon', name_long='!![en]Icon')