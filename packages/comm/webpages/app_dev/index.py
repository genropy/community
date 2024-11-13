# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires = 'frameindex'
    css_requires = 'mobile,community'       #Facciamo solo qui il css_require
    device_mode = 'mobile'                  #Specifichiamo modalità mobile
    hideLeftPlugins = True                  #Menu chiuso all'apertura della pagina
    indexTab = 'profile'                    #DP Dovrebbe aprire subito il profilo? Non funziona, lo sto facendo in un altro modo...