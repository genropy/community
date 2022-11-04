# encoding: utf-8

from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('suggestion', pkey='id', name_long='!![en]Suggestion', name_plural='!![en]Suggestion',
                                caption_field='title', survey=True)
        self.sysFields(tbl)
        
        tbl.column('title', name_long='!![en]Title')
        tbl.column('description', name_long='!![en]Description')
        tbl.column('speakers', name_long='!![en]Speakers')
        tbl.column('audience', name_long='!![en]Audience')
        tbl.column('topics', name_long='!![en]Topics')
        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('comm.developer.id', relation_name='suggestions', mode='foreignkey', onDelete='raise')
        tbl.column('suggestion_type_id',size='22', group='_', name_long='!![en]Suggestion type'
                    ).relation('comm.suggestion_type.id', relation_name='suggestions', mode='foreignkey', onDelete='setnull')
        tbl.column('suggestion_fields', dtype='X', name_long='!![en]Suggestion fields', subfields='suggestion_type_id')

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

    def defaultValues(self):
        return dict(developer_id=self.db.currentEnv.get('developer_id'))

    @public_method
    def makeInitiativeFromSuggestion(self, record=None, initiative_type=None, **kwargs):
        initiative_tbl = self.db.table(f'comm.{initiative_type}')  
        new_initiative = initiative_tbl.newrecord(suggestion_id=record['id'], **record)  
        initiative_tbl.insert(new_initiative)
        self.db.commit()