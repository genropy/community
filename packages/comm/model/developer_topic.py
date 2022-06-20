#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrbag import Bag

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('developer_topic', pkey='id', name_plural='!![en]Developer topics',
                         name_long=u'!![en]Developer topic', caption_field='topic')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='topics')
        tbl.column('topic_id',size='22',name_long = '!![en]Topic',group='_').relation('comm.topic.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')

        tbl.column('level', dtype='L',name_long='!![en]Level')
    
        tbl.aliasColumn('topic', '@topic_id.description', name_long='!![en]Topic')
        tbl.formulaColumn('caption_from_developer',"""@topic_id.description || '[' ||CAST ($level AS TEXT) || ']'""")

    def updateTopicInfo(self,developer_id=None,topic_info=None):
        self.deleteSelection('developer_id',developer_id)
        for topic_id,level in topic_info.items():
            self.insert(self.newrecord(topic_id=topic_id,level=level,developer_id=developer_id))
        
    def getTopicInfo(self,developer_id=None):
        f = self.query(where='$developer_id=:did',did=developer_id).fetch()
        result = Bag()
        for r in f:
            result[r['topic_id']] = r['level']
        return result