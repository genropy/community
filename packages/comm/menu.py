# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.thpage(u"!![en]Project types", table="comm.project_type")
        root.thpage(u"!![en]Events", table="comm.event_series")
        root.thpage(u"!![en]Event types", table="comm.event_type")
        root.lookupBranch(u"!![en]Lookups", pkg="comm")
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        root.packageBranch(u"!![en]Surveys", pkg="srvy", tags='admin')
        if self.db.application.getPreference('enable_dem', pkg='comm'):
            root.packageBranch(u"!![en]DEM", pkg="dem", tags='admin')
        root.packageBranch(u"!![en]E-mail", pkg="email", tags='admin')
        root.packageBranch(u"!![en]Administration", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"!![en]System", tags="_DEV_", pkg="sys")

    @metadata(group_code='COMM')
    def config_community(self,root,**kwargs):
        root.thpage("!![en]My profile", table='comm.developer', formResource='FormProfile',
                            pkey=self.db.currentEnv.get('developer_id'), form_locked=False)
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        root.thpage(u"!![en]Projects", table="comm.project", 
                            viewResource='ViewDevelopers', formResource='FormDevelopers')
        root.thpage(u"!![en]Events", table="comm.event_series",
                            viewResource='ViewDevelopers', formResource='FormDevelopers')

    @metadata(group_code='SUPP')
    def config_community(self,root,**kwargs):
        root.thpage("!![en]My profile", table='comm.developer', formResource='FormProfile',
                            pkey=self.db.currentEnv.get('developer_id'), form_locked=False)
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        root.thpage(u"!![en]Projects", table="comm.project", 
                            viewResource='ViewSupporters', formResource='FormSupporters')
        root.thpage(u"!![en]Events", table="comm.event_series", 
                            viewResource='ViewSupporters', formResource='FormSupporters')