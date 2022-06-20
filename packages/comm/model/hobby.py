# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('hobby', pkey='id', caption_field='description', 
                                    name_long='!![en]Hobby', name_plural='!![en]Hobbies', lookup=True)
        self.sysFields(tbl)

        tbl.column('description', name_long='!![en]Description')