from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import customizable

class ViewMobile(BaseComponent):
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('__ins_ts',hidden=True)
        r.fieldcell('send_date',hidden=True)
        r.fieldcell('subject',hidden=True)
        r.fieldcell('abstract',hidden=True)
        r.fieldcell('read',hidden=True)
        r.fieldcell('show_read',hidden=True)
        r.cell('template_row', rowTemplate="""<div>
                                                    <div style='display:flex;align-items:center;justify-content:space-between;padding-top:5px;padding-bottom:5px;'>
                                                        <div style='width:10px;margin-right:10px;'>$show_read</div>
                                                        <div style='width:100%;display: flex;justify-content: space-between;'>
                                                            <div style='font-weight:600'>$subject</div>
                                                            <div style='font-size:.9em'>$send_date</div>
                                                        </div>
                                                    </div>
                                                    <div style='font-size:80%'>$abstract</div>
                                            </div>""", width='100%')

    def th_order(self):
        return '$__ins_ts:d'
        
    def th_condition(self):
        return dict(condition='^messageFilters.condition',
                    condition_type='=messageFilters.type',
                    condition_from_date='=messageFilters.from_date',
                    condition_to_date='=messageFilters.to_date')
    
    @customizable    
    def th_top_readingstate(self, top):
        bar = top.slotToolbar('sections@readingstate,*,searchOn,5,filters', _class='mobile_bar', margin_bottom='20px')
        dlg = self.filtersDialog(bar.filters)
        bar.filters.slotButton(_class='google_icon filters', background='#555', height='35px').dataController(
                                    "dlg.show();", dlg=dlg.js_widget)
        return top
    
    def th_sections_readingstate(self):
        return [dict(code='to_read', caption='!![en]Unread', condition="$read IS NOT TRUE"),
                   dict(code='all', caption='!![en]All')]
        

    def filtersDialog(self, pane):
        dlg = pane.dialog(title='!![en]Filter messages', width='320px', height='130px', top='300px', 
                                    datapath='messageFilters', closable=True)
        fb = dlg.mobileFormBuilder(cols=2, border_spacing='4px', padding='5px')
        fb.dbSelect('^.type', table='email.message_type', lbl='!![en]Message type', colspan=2, hasDownArrow=True)
        fb.dateTextBox('^.from_date', lbl='!![en]From date')
        fb.dateTextBox('^.to_date', lbl='!![en]To date')
        dlg.dataController("""var condition_list = [];
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
                            to_date='^.to_date')
        return dlg
    
    def th_options(self):
        return dict(widget='dialog', mobileTemplateGrid=True,    
                    configurable=False,roundedEnvelope=True,
                    dialog_fullScreen=True,
                    extendedQuery=False, addrow=False, delrow=False)

    def th_options_subtable(self):
        return 'user_messages'
    

class FormMobile(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record', overflow='auto')
        bc.contentPane(region='center', margin='10px').templateChunk(
                                    table='email.message', record_id='^.id', template='msg_preview')
        
        bc.dataController("bc.widget.setRegionVisible('bottom',read)",bc=bc,read='^#FORM.record.read?=!#v')
        bc.contentPane(region='bottom').div(_class='mobile_button_container', margin_bottom='20px').lightButton(
                        '!!Mark as read', _class='mobile_button').dataRpc(self.db.table('email.message').markAsRead, 
                                                                        pkey='=#FORM.pkey', _onResult="""this.form.dismiss();""")

    def th_options(self):
        return dict(attachmentDrawer=True, modal='navigation')