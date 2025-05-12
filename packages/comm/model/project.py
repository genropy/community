# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('project', pkey='id', name_long='!![en]Project', 
                        name_plural='!![en]Projects', caption_field='title')
        self.sysFields(tbl)
        
        tbl.column('title', name_long='!![en]Title')
        tbl.column('description', name_long='!![en]Description', name_short='!![en]Descr.')
        tbl.column('app_url', name_long='!![en]Project URL')
        tbl.column('repository_url', name_long='!![en]Repository URL')
        tbl.column('start_date', dtype='D', name_long='!![en]Start date', name_short='!![en]Start')
        tbl.column('end_date', dtype='D', name_long='!![en]End date', name_short='!![en]End')
        tbl.column('project_type_id',size='22', group='_', name_long='!![en]Project type'
                    ).relation('project_type.id', relation_name='projects', mode='foreignkey', onDelete='setnull')
        tbl.column('project_fields', dtype='X', name_long='!![en]Project fields', subfields='project_type_id')
        tbl.column('suggestion_id',size='22', group='_', name_long='!![en]Suggestion'
                    ).relation('comm.suggestion.id', relation_name='projects', mode='foreignkey', onDelete='raise')
        tbl.formulaColumn('is_developer_subscribed', exists=dict(table='comm.project_developer', 
                                                                where='$developer_id=:env_developer_id AND $project_id=#THIS.id'), 
                                                                name_long='!![en]Developer is subscribed', static=True)
        tbl.column('workspace_id',size='22', group='_', name_long='!![en]Workspace'
                    ).relation('workspace.id', relation_name='projects', mode='foreignkey', onDelete='cascade')