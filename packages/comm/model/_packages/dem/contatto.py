# encoding: utf-8
from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('contatto')

        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer').relation(
                        'comm.developer.id', relation_name='contatti', one_one=True, 
                        deferred=True, mode='foreignkey', onDelete='cascade')

    def creaContattoDaDeveloper(self, developer_id, consenso_id=None):
        developer_rec = self.db.table('comm.developer').record(developer_id).output('bag')
        new_contatto = self.newrecord(nome=developer_rec['name'], cognome=developer_rec['surname'],
                                        developer_id=developer_id, consenso_id=consenso_id)
        self.insert(new_contatto)
        return(new_contatto['id'])
    
    def getSubscriptionConsent(self,contatto_id=None):
        consenso_id = self.readColumns(where='$id=:c_id', c_id=contatto_id, columns='$consenso_id')
        print(consenso_id)
        return consenso_id