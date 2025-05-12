# encoding: utf-8
from datetime import datetime
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('developer', pkey='id', name_long='!![en]Developer', name_plural='!![en]Developers',
                                    caption_field='username',survey=True)
        self.sysFields(tbl)
        
        card = tbl.colgroup('card', name_long='!![en]Card')
        pos = tbl.colgroup('position', name_long='!![en]Position')
        
        card.column('name', size=':30', name_long='!![en]Name')
        card.column('surname', size=':30', name_long='!![en]Surname',)
        tbl.column('dob', dtype='D', name_long='!![en]Date of birth')
        card.column('country', name_long='!![en]Country',)
        pos.column('position', name_long='!![en]Geocode')
        pos.column('locality', name_long='!![en]Locality')
        pos.column('region', name_long='!![en]Region')
        pos.column('state', name_long='!![en]State')
        pos.column('city', name_long='!![en]City')
        pos.column('full_address', name_long='!![en]Full address')
        tbl.column('photo_url',dtype='P', name_long='!![en]Photo')
        tbl.column('bio', name_long='!![en]Bio')
        tbl.column('tg_username', name_long='!![en]Telegram username')
        tbl.column('nickname', name_long='!![en]Nickname')
        tbl.column('github', name_long='!![en]Github')
        tbl.column('badge_id',size='22', group='_', name_long='!![en]Badge'
                    ).relation('comm.badge.id', relation_name='developers', mode='foreignkey', onDelete='setnull')
        tbl.column('user_id',size='22', group='_', name_long='!![en]User',unique=True
                    ).relation('adm.user.id', one_one='*', mode='foreignkey', onDelete='raise')
        tbl.column('organization_id',size='22', group='_', name_long='!![en]Organization'
                    ).relation('organization.id', relation_name='developers', mode='foreignkey', onDelete='setnull')
        pos.column('address_bag','X', name_long='Address bag')

        card.aliasColumn('email', '@user_id.email', name_long='!![en]Email')
        tbl.formulaColumn('fullname',"$name || ' ' || $surname", name_long='!!Fullname')
        tbl.formulaColumn('username',"COALESCE($tg_username,@user_id.username,$nickname)", name_long='!!Username')
        tbl.aliasColumn('contatto_id', '@contatti.id', name_long='!![en]Contatto', static=True)
        tbl.aliasColumn('badge_icon', '@badge_id.icon', name_long='!![en]Badge icon')
        tbl.formulaColumn('dev_badge', """'<div><img src="/_rsrc/common/css_icons/svg/16/'||$badge_icon||'" width="15px" style="margin-right\\:3px">' ||@badge_id.description||'</div>'""")
        tbl.pyColumn('dev_template', py_method='templateColumn', template_name='dev_row')

        tbl.formulaColumn('caption_name', 'COALESCE($fullname,$username)', name_long='!![en]Caption name')  
        tbl.formulaColumn('dev_location', """CASE WHEN $country IS NOT NULL AND $country != 'IT' THEN $country
                                                WHEN $locality IS NOT NULL AND $region IS NOT NULL THEN ($locality || ', ' || $region)
                                                ELSE NULL END""", name_long='!![en]Developer location')
        tbl.formulaColumn('languages',"array_to_string(ARRAY(#lang),', ')",
                            select_lang=dict(table='comm.developer_language',
                                                    columns='$caption_from_developer',
                                                    where='$developer_id=#THIS.id',
                                                    order_by='$level desc'), 
                                                    name_long='!![en]Languages')
        tbl.formulaColumn('qualifications',"array_to_string(ARRAY(#qual),', ')",
                            select_qual=dict(table='comm.developer_qualification',
                                                    columns='$caption_from_developer',
                                                    where='$developer_id=#THIS.id'),
                                                    name_long='!![en]Qualifications')
        tbl.formulaColumn('topics',"array_to_string(ARRAY(#topic),', ')",
                            select_topic=dict(table='comm.developer_topic',
                                                    columns='$topic',
                                                    where='$developer_id=#THIS.id',
                                                    order_by='$level DESC'),
                                                    name_long='!![en]Topics')
        tbl.formulaColumn('hobbies',"array_to_string(ARRAY(#hobby),', ')",
                            select_hobby=dict(table='comm.developer_hobby',
                                                    columns='$caption_from_developer',
                                                    where='$developer_id=#THIS.id'),
                                                    name_long='!![en]Hobbies')

    def createDeveloper(self,user_record):
        if self.checkDuplicate(user_id=user_record['id']):
            #existing developer with the same user_id
            return
        new_developer = self.newrecord(name = user_record['firstname'],
                            surname = user_record['lastname'], 
                            user_id = user_record['id'], 
                            badge_id=self.db.application.getPreference('user_default_badge', pkg='comm'))
        self.insert(new_developer)

    def trigger_onDeleted(self, record):
        if record['user_id']:
            self.db.table('adm.user').deleteSelection(where='$id=:u_id', u_id=record['user_id'])

    def createNewDeveloperInterview(self, survey_id=None):
        interviewtbl = self.db.table('srvy.interview')
        new_interview = interviewtbl.newrecord(survey_id=survey_id, developer_id=self.db.currentEnv['developer_id'])
        interviewtbl.insert(new_interview)
        self.db.commit()
        return new_interview['id']

    @public_method
    def deleteDeveloper(self, developer_id=None, delete_request=None):
        if not delete_request or not developer_id:
            return
        with self.recordToUpdate(developer_id) as rec:
            user_id = rec['user_id']
            rec.update({key: None for key in rec.keys()[5:]})
            rec['__del_ts'] = datetime.now()
        self.db.table('adm.user').deleteSelection(where='$id=:u_id', u_id=user_id)
        self.db.commit()
        print('**Richiesta eliminazione developer completata: ', developer_id)
        return developer_id