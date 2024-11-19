# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('message')
        
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('comm.developer.id', relation_name='messages', mode='foreignkey', onDelete='raise')
        
        tbl.column('read', name_long='!![en]Read', dtype='B')
        tbl.formulaColumn('show_read', """CASE WHEN $read IS NOT TRUE THEN '<div style="border-radius\\:10px;background\\:var(--root-primary-color);height\\:10px;width\\:10px"></div>'
                                                ELSE NULL END""")
        tbl.pyColumn('full_external_url', name_long='!![en]Full external url')

    def pyColumn_full_external_url(self,record,field):
        return self.db.application.site.externalUrl('/index', menucode='messages')
        
        
    @public_method
    def markAsRead(self, pkey):
        with self.recordToUpdate(pkey) as message_rec:
            message_rec['read'] = True
        self.db.commit()