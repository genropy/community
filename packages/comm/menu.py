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
        default_srvy = self.application.getPreference('default_srvy', pkg='comm')
        if default_srvy:
            self.developerInterview(root, survey_id=default_srvy)
    
    def developerInterview(self, root, survey_id=None):
        interview_id = self.db.table('srvy.interview').readColumns(
                                        where='$developer_id=:env_developer_id', columns='$id')
        if not interview_id:
            interview_id = self.db.table('srvy.interview').createNewDeveloperInterview(survey_id=survey_id)
            item_lbl = "!![en]Start interview"
        else:
            item_lbl = "!![en]Edit/update interview"
        root.webpage(item_lbl, filepath='/srvy/interview', url_interview_id=interview_id)