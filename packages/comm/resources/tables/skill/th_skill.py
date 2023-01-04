#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewRating(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('id',hidden=True)
        r.fieldcell('description',width='100%')
        r.checkboxcolumn('free', name='!![en]Free', width='6em')
        r.checkboxcolumn('payment', name='!![en]Payment', width='6em')
        r.checkboxcolumn('mentoring', name='!![en]Mentoring', width='6em')
        r.checkboxcolumn('speaker', name='!![en]Speaker', width='6em')
    
    def th_order(self):
        return 'id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

    def th_view(self,view):
        view.dataController(
            """
             if(_triggerpars.kw.reason=='loadData'){
                return
             }
            store.digest('#a').forEach(function(attr){
                attr = attr[0]
                skill_info.pop(attr.id)
                for(let k in attr){
                    let attr_value = attr[k];
                    if(attr_value===true){
                        let provisioning = k.split(',');
                        if(provisioning){
                            skill_info.addItem(attr.id,provisioning);
                        }
                    }
                }
            })
            """,
            skill_info='=#FORM.record.skill_info',
            store='^.store',_delay=1,_if='store'
        )

        view.dataController(
            """
            if(_triggerpars.kw.reason=='loadData' && store.len()){
                store.forEach(function(n){
                    let provisioning = skill_info.getItem(n.attr.id);
                    console.log(provisioning);
                    if(provisioning){
                        let upddict = {};
                        for(const k of provisioning.split(',')){
                            upddict[k] = true;
                        };
                    n.updAttributes(upddict,false);
                    };
                });
            }
            """,
            skill_info='=#FORM.record.skill_info',
            store='^.store'
        )

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('description')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
