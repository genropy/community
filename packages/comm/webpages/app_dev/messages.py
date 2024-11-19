# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        th = root.contentPane(region='center', datapath='main').dialogTableHandler(
            table='email.message',
            viewResource='ViewApp',
            formResource='FormApp',
            condition='^messageFilters.condition',
            condition_tipo='=messageFilters.type',
            condition_dal='=messageFilters.from_date',
            condition_al='=messageFilters.to_date',
            condition__onStart=True,
            mobileTemplateGrid=True,    
            configurable=False,roundedEnvelope=True,
            dialog_fullScreen=True,
            searchOn=True, addrow=False, delrow=False,
            **kwargs)
        
        bar = th.view.top.bar.replaceSlots('searchOn', 'filters,searchOn')
        dlg = self.filtersDialog(bar.filters)
        bar.filters.slotButton(_class='google_icon filters', background='#555', height='35px').dataController(
                                    "dlg.show();", dlg=dlg.js_widget)

    def filtersDialog(self, pane):
        dlg = pane.dialog(title='!![en]Filter messages', width='320px', height='130px', top='300px', 
                                    datapath='messageFilters', closable=True)
        fb = dlg.mobileFormBuilder(cols=2, border_spacing='4px', padding='5px')
        fb.dbSelect('^.type', table='email.message_type', lbl='!![en]Message type', colspan=2, hasDownArrow=True)
        fb.dateTextBox('^.from_date', lbl='!![en]From date')
        fb.dateTextBox('^.to_date', lbl='!![en]To date')
        dlg.dataController("""var condition_list = ['$developer_id=:env_developer_id'];
                            if(type){
                                condition_list.push('$message_type=:type');
                            };
                            if(from_date){
                                condition_list.push('$send_date>=:from_date');
                            };
                            if(to_date){
                                condition_list.push('$send_date<=:to_date');
                            };
                            var condition = condition_list.join(" AND ");
                            SET .condition = condition;
                            """, 
                            type='^.type',
                            from_date='^.from_date',
                            to_date='^.to_date',
                            _onStart=True)
        return dlg