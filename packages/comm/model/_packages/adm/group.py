# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):

    @metadata(mandatory=True)
    def sysRecord_COMM(self):
        return self.newrecord(code='COMM', description='!![en]Community Developer')