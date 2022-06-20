#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrbag import Bag

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('developer_hobby', pkey='id', name_plural='!![en]Developer hobbies',
                         name_long=u'!![en]Developer hobby', caption_field='hobby')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='hobbies')
        tbl.column('hobby_id',size='22',name_long = '!![en]Hobby',group='_').relation('comm.hobby.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        
        tbl.column('level', dtype='L',name_long='!![en]Level')
        
        tbl.aliasColumn('hobby', '@hobby_id.description', name_long='!![en]Hobby')
        tbl.formulaColumn('caption_from_developer',"""@hobby_id.description || '[' ||CAST ($level AS TEXT) || ']'""")

    def updateHobbyInfo(self,developer_id=None,hobby_info=None):
        self.deleteSelection('developer_id',developer_id)
        for hobby_id,level in hobby_info.items():
            self.insert(self.newrecord(hobby_id=hobby_id,level=level,developer_id=developer_id))
        
    def getHobbyInfo(self,developer_id=None):
        f = self.query(where='$developer_id=:did',did=developer_id).fetch()
        result = Bag()
        for r in f:
            result[r['hobby_id']] = r['level']
        return result