# encoding: utf-8

from gnr.core.gnrdecorator import metadata

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('workspace_type', pkey='code', name_long='!![en]Workspace type', 
                            name_plural='!![en]Workspace types', caption_field='name', lookup=True)
        self.sysFields(tbl)

        tbl.column('code', name_long='!![en]Code', size=':4')
        tbl.column('name', name_long='!![en]Name')
        tbl.column('repo_url', name_long='!![en]Repo url')
        
    @metadata(mandatory=True)
    def sysRecord_BITB(self):
        return self.newrecord(code='BITB', name='!![en]Bitbucket', repo_url='https://bitbucket.org/')

    @metadata(mandatory=True)
    def sysRecord_GITH(self):
        return self.newrecord(code='GITH', name='!![en]Github', repo_url='https://github.com/')

    @metadata(mandatory=True)
    def sysRecord_GITL(self):
        return self.newrecord(code='GITL', name='!![en]GitLAB', repo_url='https://gitlab.com/')