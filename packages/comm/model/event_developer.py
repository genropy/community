#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrdecorator import public_method

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('event_developer', pkey='id', name_plural='!![en]Event developers',
                         name_long=u'!![en]Event developer', caption_field='event_name')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='events')
        tbl.column('event_id',size='22',name_long = '!![en]event',group='_').relation('comm.event.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        tbl.column('role_id',size='22',name_long='!![en]Role').relation('comm.role.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='event_developers')

        tbl.aliasColumn('event_name', '@event_id.name', name_long='!![en]Event name')

    @public_method
    def subscribeToevent(self, event_id=None, developer_id=None):
        if not event_id or not developer_id:
            return
        new_subscription = self.newrecord(event_id=event_id, developer_id=developer_id)
        self.insert(new_subscription)
        self.db.commit()