# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('skill', pkey='id', caption_field='description', 
                                    name_long='!![en]Skill', name_plural='!![en]Skills', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_long='!![en]Description')