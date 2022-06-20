#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewRating(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code',hidden=True)
        r.fieldcell('description',width='100%')
        level = r.columnset('level',name='!![en]Level')
        level.checkboxcolumn('level_0',radioButton='level',
                        name=u'!![en]No',width='4em')
        level.checkboxcolumn('level_1',radioButton='level',
                        name=u'!![en]Low',width='4em')
        level.checkboxcolumn('level_2',radioButton='level',
                        name=u'!![en]Medium',width='4em')
        level.checkboxcolumn('level_3',radioButton='level',
                        name=u'!![en]Good',width='4em')
        level.checkboxcolumn('level_4',radioButton='level',
                        name=u'!![en]Excellent',width='6em')

    def th_order(self):
        return 'code'

    def th_query(self):
        return dict(column='code', op='contains', val='')


    def th_view(self,view):
        view.dataController(
            """
             if(_triggerpars.kw.reason=='loadData'){
                return
             }
            store.digest('#a').forEach(function(attr){
                attr = attr[0]
                language_info.pop(attr.code)
                for(let k in attr){
                    let attr_value = attr[k];
                    if(attr_value===true){
                        let level = parseInt(k.slice(6));
                        if(level){
                            language_info.addItem(attr.code,level);
                        }
                    }
                }
            })
            """,
            language_info='=#FORM.record.language_info',
            store='^.store',_delay=1,_if='store'
        )

        view.dataController(
            """
            if(_triggerpars.kw.reason=='loadData' && store.len()){
                store.forEach(function(n){
                    let level = language_info.getItem(n.attr.code);
                    if(level){
                        let upddict = {};
                        upddict['level_'+level] = true;
                        n.updAttributes(upddict,false);
                    }
                });
            }
            """,
            language_info='=#FORM.record.language_info',
            store='^.store'
        )



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('code')
        fb.field('description')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
