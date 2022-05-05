# encoding: utf-8
from sys import implementation
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('workspace', pkey='id', name_long='!![en]Workspace', name_plural='!![en]Workspace',
                        caption_field='code', lookup=True)
        self.sysFields(tbl)
        
        tbl.column('code', name_long='!![en]Code')
        tbl.column('description', name_long='!![en]Description')
        tbl.column('link', name_long='Link')
        tbl.column('workspace_metadata', dtype='X', name_long='Workspace metadata')
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('developer.id', relation_name='workspaces', mode='foreignkey', onDelete='raise')

    @public_method
    def getWorkspaces(self, service_name=None, service_type=None, developer_id=None):
        repo_service = self.db.application.site.getService(service_name=service_name, service_type=service_type)
        assert repo_service,'set in siteconfig the service'
        workspaces = repo_service.getWorkspaces()
        for w in workspaces.digest('#v'):
                workspace_code = w['workspace']['slug']
                workspace_link = w['workspace']['links.html.href']
                workspace_record = self.newrecord(code=workspace_code, 
                                    link=workspace_link, developer_id=developer_id,
                                    workspace_metadata=w)
                self.insert(workspace_record)
                self.db.commit()
                print('**Bitbucket workspace added: ', workspace_code)
        return workspaces