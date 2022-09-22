#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrdecorator import public_method

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('project_developer', pkey='id', name_plural='!![en]Project developers',
                         name_long=u'!![en]Project developer', caption_field='project')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='projects')
        tbl.column('project_id',size='22',name_long = '!![en]Project',group='_').relation('comm.project.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        tbl.column('role_id',size='22',name_long='!![en]Role').relation('comm.role.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='project_developers')

    @public_method
    def subscribeToProject(self, project_id=None, developer_id=None):
        if not project_id or not developer_id:
            return
            #Da finire
        