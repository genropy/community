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
        tbl.column('workspace_metadata', dtype='X', name_long='Workspace metadata')
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('developer.id', relation_name='workspaces', mode='foreignkey', onDelete='cascade')
    
    @public_method
    def getWorkspaces(self, repo_service=None, developer_id=None):
        service_type, service_name = repo_service.split('_')
        repo_service = self.db.application.site.getService(service_name=service_name, service_type=service_type)
        assert repo_service,'set in siteconfig the service'
        workspaces = repo_service.getWorkspaces()
        if not workspaces:
            user_data = repo_service.getUser()
            username = self.createWorkspaceForUserData(user_data, developer_id=developer_id)
            return username
        for w in workspaces.digest('#v'):
            self.createNewWorkspace(w, developer_id=developer_id)
        return workspaces

    def createNewWorkspace(self, w, developer_id=None):
        workspace_code = w['workspace']['slug']
        workspace_link = w['workspace']['links.html.href']
        workspace_record = self.newrecord(code=workspace_code, 
                            link=workspace_link, developer_id=developer_id,
                            workspace_metadata=w)
        self.insert(workspace_record)
        self.db.commit()
        print('**Workspace added: ', workspace_code)
        return workspace_code

    def createWorkspaceForUserData(self, user_data, developer_id=None):
        workspace_code = user_data['login']
        workspace_link = user_data['html_url']
        workspace_record = self.newrecord(code=workspace_code, 
                            link=workspace_link, developer_id=developer_id,
                            workspace_metadata=user_data)
        self.insert(workspace_record)
        self.db.commit()
        print('**Workspace added for user ', workspace_code)
        return workspace_code