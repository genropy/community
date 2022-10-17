#!/usr/bin/env python
# encoding: utf-8

from datetime import time

class GnrCustomWebPage(object):
    py_requires="""public:Public,iframegallery/iframegallery:IframeGallery"""
    pageOptions = dict(openMenu=False,enableZoom=False)
    auth_main='user'

    def configuration(self):
        return [
            {'title':'!!Home','url':'/adm/home'},
            {'title':'!!Profile','url':'/comm/profile'},
            {'title':'!!Community Map','url':'/comm/community_map'}
        ]