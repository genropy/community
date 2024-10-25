# encoding: utf-8
from sys import implementation
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('workspace', pkey='id', name_long='!![en]Workspace', name_plural='!![en]Workspace',
                        caption_field='code')
        self.sysFields(tbl)
        
        tbl.column('code', name_long='!![en]Code')
        tbl.column('description', name_long='!![en]Description')
        tbl.column('link', name_long='Link')
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('developer.id', relation_name='workspaces', mode='foreignkey', onDelete='cascade')