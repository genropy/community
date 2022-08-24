# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.lookupBranch(u"!![en]Lookups", pkg="comm")
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        root.packageBranch(u"!![en]Surveys", pkg="srvy", tags='admin')
        root.packageBranch(u"!![en]DEM", pkg="dem", tags='admin')
        root.packageBranch(u"!![en]E-mail", pkg="email", tags='admin')
        root.packageBranch(u"!![en]Administration", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"!![en]System", tags="_DEV_", pkg="sys")

    @metadata(group_code='COMM')
    def config_community(self,root,**kwargs):
        root.thpage("!![en]My profile", table='comm.developer', formResource='FormProfile',
                            pkey=self.db.currentEnv.get('developer_id'), form_locked=False)
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        self.developerInterview(root)
    
    def developerInterview(self, root):
        interview_id = self.db.table('srvy.interview').readColumns(where='$developer_id=:env_developer_id', 
                                                                    columns='$id')
        if not interview_id:
            root.thpage(u"!![en]Start Interview", table='srvy.interview', 
                                                    pkey='*newrecord*', formResource='InterviewStartForm')
        else:
            root.thpage(u"!![en]Update Interview", table='srvy.interview', 
                                                    pkey=interview_id, formResource='InterviewStartForm')