# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Menu(object):
    def config(self,root,**kwargs):
        root.thpage("!![en]My profile", table='comm.developer', pkey=self.db.currentEnv.get('developer_id'))
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.webpage(u"!![en]Community map", filepath="/comm/community_map")
        root.lookupBranch("!![en]Lookups", pkg="comm")
        root.packageBranch(u"!![en]Surveys", pkg="srvy", tags='admin')
        root.packageBranch(u"!![en]Administration", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"!![en]System", tags="_DEV_", pkg="sys")

    @metadata(group_code='COMM')
    def config_developers(self,root,**kwargs):
        root.thpage("!![en]My profile", table='comm.developer', pkey=self.db.currentEnv.get('developer_id'))
        root.thpage(u"!![en]Developers", table="comm.developer", viewResource='ViewMap', formResource='FormDevelopers')
        root.thpage(u"!![en]Projects", table="comm.project")
        root.webpage(u"!![en]Community map", filepath="/comm/community_map")