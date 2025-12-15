# encoding: utf-8
from subscription_token import generate_token

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('user')
        
        tbl.colgroup('repo_token', name_long='!![en]Repository tokens')
        tbl.column('repo_subscription_token', size='32', name_long='!![en]Subscription token', name_short='!![en]Token')
        tbl.column('repo_token_creation_date', dtype='D', name_long='!![en]Subscription token creation date', name_short='!![en]Token creation')
        
    
    def userSubscriptionToken(self, record, refresh=False):
        with self.db.table('adm.user').recordToUpdate(record['user_id']) as user:
            if refresh or not user['repo_subscription_token']:
                user['repo_subscription_token'] = generate_token(32) #sys external token?
                user['repo_token_creation_date'] = self.db.workdate