# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        root.thFormHandler(datapath='main',
            table='comm.developer',
            startKey=self.rootenv['developer_id'],
            formResource='FormProfile',
            form_locked=False
        )