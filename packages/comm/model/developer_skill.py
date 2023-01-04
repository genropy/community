#!/usr/bin/env python
# encoding: utf-8

from gnr.core.gnrbag import Bag

class Table(object):
    
    def config_db(self, pkg):
        tbl =  pkg.table('developer_skill', pkey='id', name_plural='!![en]Developer skills',
                         name_long=u'!![en]Developer skill', caption_field='skill')
        self.sysFields(tbl)
        
        tbl.column('developer_id',size='22',name_long = '!![en]Developer',group='_').relation('comm.developer.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='skills')
        tbl.column('skill_id',size='22',name_long = '!![en]skill',group='_').relation('comm.skill.id',
                                                                                    onDelete='cascade',
                                                                                    mode='foreignkey',
                                                                                    relation_name='developers')
        
        tbl.column('provisioning',name_long='!![en]Provisioning')

        tbl.aliasColumn('skill', '@skill_id.description', name_long='!![en]Skill')
        tbl.formulaColumn('caption_from_developer',"""@skill_id.description || '[' ||CAST ($level AS TEXT) || ']'""")

    def updateSkillInfo(self, developer_id=None, skill_info=None):
        self.deleteSelection('developer_id',developer_id)
        for skill_id,provisioning in skill_info.items():
            self.insert(self.newrecord(skill_id=skill_id, developer_id=developer_id, provisioning=provisioning))
        
    def getSkillInfo(self,developer_id=None):
        f = self.query(where='$developer_id=:did',did=developer_id, columns='$skill_id,$provisioning', 
                                                    group_by='$skill_id,$provisioning').fetchGrouped('skill_id')
        result = Bag()
        for r in f.values():
            provisioning = ','.join([p['provisioning'] for p in r]) 
            result.setItem(r[0]['skill_id'],provisioning)
        return result