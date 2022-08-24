# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('interview')

        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('comm.developer.id', relation_name='interviews', mode='foreignkey', onDelete='cascade')