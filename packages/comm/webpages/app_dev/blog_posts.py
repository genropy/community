# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        root.dialogTableHandler(datapath='main',
            table='wordpress.post',
            viewResource='ViewApp',
            formResource='FormApp',
            view_store_onStart=True,
            mobileTemplateGrid=True,     
            configurable=False, 
            roundedEnvelope=True,
            dialog_fullScreen=True,
            searchOn=True, addrow=False, delrow=False,
            **kwargs)
    