#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='Community package',sqlschema='comm',sqlprefix=True,
                    name_short='!![en]Community', name_long='!![en]Community', name_full='!![en]Community')
                    
    def config_db(self, pkg):
        pass
    
    def required_packages(self):
        return ['gnrcore:email']
    
        
class Table(GnrDboTable):
    pass
