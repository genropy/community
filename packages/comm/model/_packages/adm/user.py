# encoding: utf-8

class Table(object):

    def config_db(self,pkg):
        tbl=pkg.table('user')
        tbl.column('newsletter', dtype='B', name_long='!![en]Newsletter')

    def trigger_onUpdating(self,record,old_record=None):
        if old_record['status'] != 'conf' and record['status'] == 'conf':
            group_code = self.db.table('adm.group').sysRecord('COMM')['code']
            record['group_code'] = group_code
            self.db.table('comm.developer').createDeveloper(record)
            if record['newsletter']:
                self.subscribeToNewsletter(record['user_id'])
        if not old_record['newsletter'] and record['newsletter']:
            self.subscribeToNewsletter(record['email'])

    def subscribeToNewsletter(self, email):
        contatto_tbl = self.db.table('dem.contatto')
        iscrizione_tbl = self.db.table('dem.contatto_lista')
        existing_email = contatto_tbl.readColumns(where='$email=:email', columns='$email', email=email)
        if existing_email:
            return 'Utente già iscritto.'
        else: 
            user_data = self.record(where='$email=:email', email=email).output('bag')                                             
            new_contatto = contatto_tbl.newrecord(nome=user_data['firstname'], cognome=user_data['lastname'], 
                            email=email, consenso_id='Newsletter____________')
            contatto_tbl.insert(new_contatto)
            new_iscritto = iscrizione_tbl.newrecord(contatto_id=new_contatto['id'], 
                            lista_id=self.getPreference('newsletter_list', pkg='comm'))
            #DP Lista default nelle preferenze
            iscrizione_tbl.insert(new_iscritto)
            self.db.commit()                                                    
            return 'Utente iscritto.'