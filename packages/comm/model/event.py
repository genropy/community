# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('event', pkey='id', name_long='!![en]Event', 
                        name_plural='!![en]Events', caption_field='name')
        self.sysFields(tbl)
        
        tbl.column('name', name_long='!![en]Name')
        tbl.column('description', name_long='!![en]Description', name_short='!![en]Descr.')
        tbl.column('event_url', name_long='!![en]Event URL')
        tbl.column('start_date', dtype='DH', name_long='!![en]Start date', name_short='!![en]Start')
        tbl.column('end_date', dtype='DH', name_long='!![en]End date', name_short='!![en]End')
        tbl.column('event_series_id',size='22', group='_', name_long='!![en]Event series'
                    ).relation('event_series.id', relation_name='events', mode='foreignkey', onDelete='cascade')
        tbl.column('suggestion_id',size='22', group='_', name_long='!![en]Suggestion'
                    ).relation('comm.suggestion.id', relation_name='events', mode='foreignkey', onDelete='raise')

        tbl.aliasColumn('event_type_id', '@event_series_id.event_type_id', name_long='!![en]Event type')
        tbl.formulaColumn('is_developer_subscribed', exists=dict(table='comm.event_developer', 
                                                                where='$developer_id=:env_developer_id AND $event_id=#THIS.id'), 
                                                                name_long='!![en]Developer is subscribed', static=True)