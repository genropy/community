#!/usr/bin/env python
# encoding: utf-8
from gnr.core.gnrbag import Bag

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('developer_language', pkey='id', name_plural='!![en]Developer languages',
                         name_long=u'!![en]Developer language', caption_field='language')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='languages')
        tbl.column('language_code',size=':3',name_long = '!![en]Language',group='_').relation('comm.language.code',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        tbl.column('level', dtype='L',name_long='!![en]Level')

        tbl.aliasColumn('language', '@language_code.description', name_long='!![en]Programming language')
        tbl.formulaColumn('caption_from_developer',"""@language_code.description || '[' ||CAST ($level AS TEXT) || ']'""")

    def updateLanguageInfo(self,developer_id=None,language_info=None):
        self.deleteSelection('developer_id',developer_id)
        for language_code,level in language_info.items():
            self.insert(self.newrecord(language_code=language_code,level=level,developer_id=developer_id))
        
    def getLanguageInfo(self,developer_id=None):
        f = self.query(where='$developer_id=:did',did=developer_id).fetch()
        result = Bag()
        for r in f:
            result[r['language_code']] = r['level']
        return result