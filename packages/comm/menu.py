# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Developers", table="comm.developer")
        root.thpage(u"!![en]Projects", table="comm.project")
        root.packageBranch(u"Amministrazione sito", tags="superadmin,_DEV_", pkg="adm")
        root.packageBranch(u"Sistemistica", tags="_DEV_", pkg="sys")