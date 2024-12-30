
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class ViewApp(BaseComponent):

    def th_hiddencolumns(self):
        return '$date,$time,$title,$message,$category,$ext_link_template'
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.cell('post_template', width='auto', rowTemplate="""<div style='display:flex;align-items:center;padding-top:5px;padding-bottom:5px;justify-content:space-between;width:100%'>
                                                                    <div style='display:flex;'>
                                                                        <div style='font-size:0.9em;margin-right:5px'>$date</div>  
                                                                        <div>$title</div>  
                                                                    </div>
                                                                    <div style='font-weight:bold;'>$category</div>
                                                                </div>""")
        
    def th_condition(self):
        return dict(published=True)
    
    def th_order(self):
        return 'date:DESC'
    
class FormApp(BaseComponent):
    py_requires='docu_components:ContentsComponent,gnrcomponents/attachmanager/attachmanager:AttachManager'
    css_requires='social'

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        self.contentText(bc.contentPane(region='center', datapath='.@content_id', overflow='hidden', padding='20px'), 
                         viewer=True, _class='selectable')
        
        footer = form.bottom.slotToolbar('*,post_links,*', _class='mobile_toolbar')
        footer.post_links.div('^#FORM.record.ext_link_template', _virtual_column='ext_link_template')

    def th_options(self):
        return dict(modal='navigation', showtoolbar=False, readOnly=False)