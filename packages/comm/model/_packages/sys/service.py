# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('service')

        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('comm.developer.id', relation_name='services', mode='foreignkey', onDelete='cascade')

        tbl.aliasColumn('username', '@developer_id.username', name_long='!![en]Username')

    def trigger_onInserting(self, record, old_record=None):
        if not record['developer_id']:
            record['developer_id'] = self.db.currentEnv['developer_id']
        if record['service_type'] == 'repository':
            username = self.db.table('comm.developer').readColumns(record['developer_id'], columns='$username')
            record['service_name'] = record['implementation'] + '-' + username
            record['service_identifier'] = record['service_type'] + '_' + record['service_name']