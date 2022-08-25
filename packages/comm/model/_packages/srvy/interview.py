# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('interview')

        tbl.column('developer_id',size='22', group='_', name_long='!![en]Developer'
                    ).relation('comm.developer.id', relation_name='interviews', mode='foreignkey', onDelete='cascade')

    def createNewDeveloperInterview(self, survey_id=None):
        new_interview = self.newrecord(survey_id=survey_id, developer_id=self.db.currentEnv['developer_id'])
        self.insert(new_interview)
        self.db.commit()
        return new_interview['id']