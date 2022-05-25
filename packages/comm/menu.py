# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.webpage(u"!![en]Community map", filepath="/comm/community_map")
        root.lookupBranch("!![en]Lookups", pkg="comm")
        root.packageBranch(u"!![en]Surveys", pkg="srvy")
        root.packageBranch(u"!![en]Administration", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"!![en]System", tags="_DEV_", pkg="sys")