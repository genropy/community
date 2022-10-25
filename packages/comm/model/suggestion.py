# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('suggestion', pkey='id', name_long='!![en]Suggestion', name_plural='!![en]Suggestion',
                                caption_field='title', survey=True)
        self.sysFields(tbl)
        
        tbl.column('title', name_long='!![en]Title')
        tbl.column('description', name_long='!![en]Description')
        tbl.column('speakers', name_long='!![en]Speakers')
        tbl.column('audience', name_long='!![en]Audience')
        tbl.column('suggestion_type_id',size='22', group='_', name_long='!![en]Suggestion type'
                    ).relation('comm.suggestion_type.id', relation_name='suggestions', mode='foreignkey', onDelete='setnull')

        tbl.formulaColumn('is_developer_interested', exists=dict(table='comm.suggestion_developer', 
                                                                where='$developer_id=:env_developer_id AND $suggestion_id=#THIS.id'), 
                                                                name_long='!![en]Developer is interested', static=True)
        tbl.formulaColumn('how_many_interested', select=dict(table='comm.suggestion_developer', 
                                                                where='$suggestion_id=#THIS.id', columns='COUNT(*)'),
                                                                name_long='!![en]How many are interested')
        tbl.aliasColumn('is_project', '@projects.id', name_long='!![en]Is project')
        tbl.aliasColumn('is_meeting', '@meetings.id', name_long='!![en]Is meeting')
        tbl.aliasColumn('is_event', '@events.id', name_long='!![en]Is event')
        tbl.formulaColumn('approved', '$is_project || $is_meeting || $is_event', name_long='!![en]Approved')
