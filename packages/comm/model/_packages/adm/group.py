# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):

    @metadata(mandatory=True)
    def sysRecord_COMM(self):
        return self.newrecord(code='COMM', description='!![en]Community Developer', rootpage='/comm/app_dev/index')

    @metadata(mandatory=True)
    def sysRecord_SUPP(self):
        return self.newrecord(code='SUPP', description='!![en]Community Supporter')