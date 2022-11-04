#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrdecorator import public_method

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('meeting_developer', pkey='id', name_plural='!![en]Meeting developers',
                         name_long=u'!![en]Meeting developer', caption_field='meeting_title')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='meetings')
        tbl.column('meeting_id',size='22',name_long = '!![en]event',group='_').relation('comm.meeting.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        tbl.column('role_id',size='22',name_long='!![en]Role').relation('comm.role.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='meeting_developers')

        tbl.aliasColumn('meeting_title', '@meeting_id.title', name_long='!![en]Event title')
        tbl.aliasColumn('role_icon', '@role_id.icon', name_long='!![en]Role icon')

    @public_method
    def subscribeToevent(self, meeting_id=None, developer_id=None):
        if not meeting_id or not developer_id:
            return
        new_subscription = self.newrecord(meeting_id=meeting_id, developer_id=developer_id)
        self.insert(new_subscription)
        self.db.commit()