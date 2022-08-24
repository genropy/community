# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('developer', pkey='id', name_long='!![en]Developer', name_plural='!![en]Developers',
                                    caption_field='tg_username')
        self.sysFields(tbl)
        
        tbl.column('name', size=':30', name_long='!![en]Name', group='card')
        tbl.column('surname', size=':30', name_long='!![en]Surname',group='card')
        tbl.column('email', name_long='Email',group='card')
        tbl.column('country', name_long='!![en]Country',group='card')
        tbl.column('position', name_long='!![en]Geocode')
        tbl.column('locality', name_long='!![en]Locality')
        tbl.column('region', name_long='!![en]Region')
        tbl.column('state', name_long='!![en]State')
        tbl.column('city', name_long='!![en]City')
        tbl.column('full_address', name_long='!![en]Full address')
        tbl.column('photo_url',dtype='P', name_long='!![en]Photo')
        tbl.column('bio', name_long='!![en]Bio')
        tbl.column('tg_username', name_long='!![en]Telegram username')
        tbl.column('nickname', name_long='!![en]Nickname')
        tbl.column('github', name_long='!![en]Github')
        tbl.column('website', name_long='!![en]Website')
        tbl.column('user_id',size='22', group='_', name_long='!![en]User',unique=True
                    ).relation('adm.user.id', one_one=True, relation_name='developer', 
                         mode='foreignkey', onDelete='raise')
        
        tbl.formulaColumn('fullname',"$name || ' ' || $surname", name_long='Fullname')
        tbl.aliasColumn('contatto_id', '@contatti.id', name_long='!![en]Contatto', static=True)
        tbl.pyColumn('dev_template', py_method='templateColumn', template_name='dev_row')

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
                                                    columns='$caption_from_developer',
                                                    where='$developer_id=#THIS.id'),
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
                            surname = user_record['lastname'], email = user_record['email'],
                            user_id = user_record['id'], )
        self.insert(new_developer)

    def trigger_onDeleted(self, record):
        if record['user_id']:
            self.db.table('adm.user').deleteSelection(where='$id=:u_id', u_id=record['user_id'])
