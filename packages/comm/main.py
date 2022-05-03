#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='comm package',sqlschema='comm',sqlprefix=True,
                    name_short='Comm', name_long='Comm', name_full='Comm')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
