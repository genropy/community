# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('event_series', pkey='id', name_long='!![en]Event series', 
                        name_plural='!![en]Events series', caption_field='name')
        self.sysFields(tbl)
        
        tbl.column('name', name_long='!![en]Name')
        tbl.column('description', name_long='!![en]Description', name_short='!![en]Descr.')
        tbl.column('event_url', name_long='!![en]Event URL')
        tbl.column('repository_url', name_long='!![en]Repository URL')
        tbl.column('event_type_id',size='22', group='_', name_long='!![en]Event type'
                    ).relation('event_type.id', relation_name='events', mode='foreignkey', onDelete='setnull')
        tbl.column('event_fields', dtype='X', name_long='!![en]Event fields', subfields='event_type_id')
        tbl.column('suggestion_id',size='22', group='_', name_long='!![en]Suggestion'
                    ).relation('comm.suggestion.id', relation_name='event_series', mode='foreignkey', onDelete='raise')