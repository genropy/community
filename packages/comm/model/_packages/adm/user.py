# encoding: utf-8

# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl = pkg.table('user', survey=True)
        
        tbl.formulaColumn('is_developer', "@developer.id IS NOT NULL", dtype='B', name_long='!![en]Is developer')

    def trigger_onUpdating(self,record,old_record=None):
        if old_record['status'] != 'conf' and record['status'] == 'conf':
            group_code = self.db.table('adm.group').sysRecord('COMM')['code']
            record['group_code'] = group_code
            self.db.table('comm.developer').createDeveloper(record)