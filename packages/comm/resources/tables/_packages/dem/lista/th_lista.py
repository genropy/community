#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewSubscription(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('id',hidden=True)
        r.fieldcell('nome',width='100%')
        r.checkboxcolumn('subscription', name=u'!![en]Subscribed', width='6em')
    
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
                newsletter_subscription.pop(attr.id)
                for(let k in attr){
                    let attr_value = attr[k];
                    if(attr_value===true){
                        newsletter_subscription.addItem(attr.id,true);
                    }
                }
            })
            """,
            newsletter_subscription='=#FORM.record.newsletter_subscription',
            store='^.store',_delay=1,_if='store'
        )

        view.dataController(
            """
            if(_triggerpars.kw.reason=='loadData' && store.len()){
                store.forEach(function(n){
                    let subscription = newsletter_subscription.getItem(n.attr.id);
                    if(subscription){
                        let upddict = {};
                        upddict['subscription'] = true;
                        n.updAttributes(upddict,false);
                    }
                });
            }
            """,
            newsletter_subscription='=#FORM.record.newsletter_subscription',
            store='^.store'
        )