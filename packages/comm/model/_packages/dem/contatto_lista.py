# encoding: utf-8
from gnr.core.gnrbag import Bag

class Table(object):

    def updateNewsletterSubscription(self, developer_id=None, newsletter_subscription=None):
        contatto_id = self.db.table('dem.contatto').readColumns(columns='$id', 
                                where='$developer_id=:did', did=developer_id, ignoreMissing=True)
        self.deleteSelection(where='$contatto_id=:c_id', c_id=contatto_id)                                    
        if not contatto_id:
            contatto_id = self.db.table('dem.contatto').creaContattoDaDeveloper(developer_id=developer_id)
        for lista_id,true in newsletter_subscription.items():
            self.insert(self.newrecord(lista_id=lista_id, contatto_id=contatto_id))
        
    def getNewsletterSubscription(self,contatto_id=None):
        liste = self.query(where='$contatto_id=:c_id', c_id=contatto_id).fetch()
        result = Bag()
        for sub in liste:
            result[sub['lista_id']] = True
        return result