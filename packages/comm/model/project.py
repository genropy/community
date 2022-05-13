# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('project', pkey='id', name_long='!![en]Project', 
                        name_plural='!![en]Projects', caption_field='name')
        self.sysFields(tbl)
        
        tbl.column('name', name_long='!![en]Name')
        tbl.column('description', name_long='!![en]Description', name_short='!![en]Descr.')
        tbl.column('app_url', name_long='!![en]Project URL', name_short='!![en]App')
        tbl.column('repository_url', name_long='!![en]Repository URL', name_short='!![en]Repo')
        tbl.column('project_metadata', dtype='X', name_long='Project metadata')
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('developer.id', relation_name='projects', mode='foreignkey', onDelete='raise')
        tbl.column('workspace_id',size='22', group='_', name_long='!![en]Workspace'
                    ).relation('workspace.id', relation_name='projects', mode='foreignkey', onDelete='raise')

    @public_method
    def getProjects(self, service_name=None, service_type=None, developer_id=None, workspace_slug=None):
        repo_service = self.db.application.site.getService(service_name=service_name, service_type=service_type)
        assert repo_service,'set in siteconfig the service'
        projects = repo_service.getProjects(workspace_slug=workspace_slug)
        if not projects:
            return
        workspace_id = self.db.table('comm.workspace').readColumns(where='$code=:w_s', 
                                    w_s=workspace_slug, columns='$id')
        for p in projects.digest('#v'):
            repository_url = p['links.html.href'] or p['url']
            name = p['name']
            description = p['description']
            workspace_record = self.newrecord(repository_url=repository_url, 
                                name=name, description=description, 
                                project_metadata=p,
                                developer_id=developer_id, workspace_id=workspace_id)
            self.insert(workspace_record)
            self.db.commit()
            print('**Project added: ', name)
        return projects