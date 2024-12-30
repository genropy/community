from gnr.web.gnrbaseclasses import BaseComponent

class ViewApp(BaseComponent):
    css_requires='mobile,community'
    
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
        
    def th_top_state(self, top):
        bar = top.bar.replaceSlots('vtitle', 'sections@readingstate')
        bar.attributes['_class'] = 'mobile_toolbar'
    
    def th_sections_readingstate(self):
        return [dict(code='NOTREAD', caption='!![en]Not read', condition="$read IS NOT TRUE"),
                   dict(code='ALL', caption='!![en]All')]
        
class FormApp(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record', overflow='auto')
        bc.contentPane(region='center', margin='10px').templateChunk(
                                    table='email.message', record_id='^.id', template='msg_preview')
        
        bc.dataController("bc.widget.setRegionVisible('bottom',read)",bc=bc,read='^#FORM.record.read?=!#v')
        bc.contentPane(region='bottom').div(_class='mobile_button_container', margin_bottom='20px').lightButton(
                        '!![en]Mark as read', _class='mobile_button').dataRpc(self.db.table('email.message').markAsRead, 
                                                                        pkey='=#FORM.pkey', _onResult="""this.form.dismiss();""")

    def th_options(self):
        return dict(attachmentDrawer=True, modal='navigation')