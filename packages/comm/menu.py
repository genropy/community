# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.thpage(u"!![en]Project types", table="comm.project_type")
        root.thpage(u"!![en]Events", table="comm.event")
        root.thpage(u"!![en]Event types", table="comm.event_type")
        root.thpage(u"!![en]Suggestions", table="comm.suggestion")
        root.thpage(u"!![en]Suggestion types", table="comm.suggestion_type")
        root.webpage(u"!![en]Community", filepath="/comm/community_map")
        root.lookupBranch(u"!![en]Lookups", pkg="comm")

    @metadata(group_code='COMM')
    def config_community(self,root,**kwargs):
        self.subMenuDevelopers(root, formResource='FormDevelopers')

    @metadata(group_code='SUPP')
    def config_supporters(self,root,**kwargs):
        self.subMenuDevelopers(root, formResource='FormSupporters')
    
    def subMenuDevelopers(self, branch, formResource=None):
        branch.webpage("!![en]My profile", filepath='/comm/app_dev/profile', openOnStart=True)
        branch.webpage(u"!![en]Community", filepath="/comm/community_map")
        branch.thpage(u"!![en]Suggestions", table="comm.suggestion")
        branch.thpage(u"!![en]Projects", table="comm.project", viewResource='ViewDevelopers', formResource=formResource)
        branch.thpage(u"!![en]Events", table="comm.event", viewResource='ViewDevelopers', formResource=formResource)

class ApplicationMenu(object):

    @metadata(group_code='COMM')
    def config_community(self,root,**kwargs):
        root.webpage("!![en]My profile", filepath='/comm/app_dev/profile', openOnStart=True)
        root.webpage('!!Messages', filepath='/email/my_messages', table='email.message', 
                         titleCounter=True, titleCounter_condition='$dest_user_id=:env_user_id AND $read IS NOT TRUE',
                         menucode='messages')
        root.webpage('!![en]Subscriptions', filepath='/repomgm/user_subscriptions')
        root.webpage(u"!![en]Community map", filepath="/comm/community_map")
        self.publicationsSubMenu(root.branch("!![en]Publications"))
        #root.thpage(u"!![en]Suggestions", table="comm.suggestion")
        #root.thpage(u"!![en]Projects", table="comm.project", viewResource='ViewDevelopers', formResource='FormDevelopers')
        #root.thpage(u"!![en]Events", table="comm.event", viewResource='ViewDevelopers', formResource='FormDevelopers')
        
    def publicationsSubMenu(self, branch):
        branch.webpage('!![en]Social posts', filepath='/comm/app_dev/social_posts', menucode='social_posts')
        branch.webpage('!![en]Blog posts', filepath='/comm/app_dev/blog_posts', menucode='blog_posts')
        
    def config(self,root,**kwargs):
        root.packageBranch(u"!![en]Community", pkg="comm")
        root.packageBranch(u"!![en]Repository management", pkg="repomgm")
        root.packageBranch(u"!![en]Surveys", pkg="srvy", tags='admin')
        if self.db.application.getPreference('enable_social', pkg='comm'):
            root.packageBranch(u"!![en]Social", pkg="social", tags='admin')
            root.packageBranch(u"!![en]Video", pkg="video", tags='admin')
            root.packageBranch('!![en]Blog', pkg='wordpress', tags='admin')
        if self.db.application.getPreference('enable_genrobot', pkg='comm'):
            root.packageBranch(u"!![en]Genrobot", pkg="genrobot", tags='admin')
        if self.db.application.getPreference('enable_dem', pkg='comm'):
            root.packageBranch(u"!![en]DEM", pkg="dem", tags='admin')
        root.packageBranch(u"!![en]E-mail", pkg="email", tags='admin')
        root.packageBranch(u"!![en]Administration", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"!![en]System", tags="_DEV_", pkg="sys")
        root.packageBranch("!![en]Web Notifications", pkg="wpn")
        root.packageBranch("!![en]Dashboard", pkg="biz")
