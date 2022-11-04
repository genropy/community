#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrdecorator import public_method

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('suggestion_developer', pkey='id', name_plural='!![en]Suggestion developers',
                         name_long=u'!![en]Suggestion developer', caption_field='suggestion_title')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='suggestions')
        tbl.column('suggestion_id',size='22',name_long = '!![en]Suggestion',group='_').relation('comm.suggestion.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')

        tbl.aliasColumn('suggestion_title', '@suggestion_id.title', name_long='!![en]Suggestion title')

    @public_method
    def interestedInSuggestion(self, suggestion_id=None, developer_id=None):
        if not suggestion_id or not developer_id:
            return
        new_subscription = self.newrecord(suggestion_id=suggestion_id, developer_id=developer_id)
        self.insert(new_subscription)
        self.db.commit()
    