# encoding: utf-8
from gnr.core.gnrdecorator import public_method

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('message')
        
        tbl.subtable('user_messages', condition='$dest_user_id=:env_user_id')
        tbl.joinColumn('dest_user_id', name_long='!!Destination user').relation('adm.user.id', 
                                cnd="""@dest_user_id.email=$to_address""", relation_name='received_messages')