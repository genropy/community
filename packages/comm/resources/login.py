from gnr.web.gnrbaseclasses import BaseComponent


class LoginComponent(BaseComponent):
            
    def onUserSelected(self, avatar, data):
        developer_id = self.db.table("comm.developer").readColumns(where='$user_id=:u_id',u_id=avatar.user_id, columns="$id")
        data.setItem("developer_id", developer_id)

    def login_newUser_form(self,form):
        fb = form.record.div(margin='10px',margin_right='20px',padding='10px').formbuilder(
                        cols=1, border_spacing='6px',onEnter='SET creating_new_user = true;',
                        width='100%',tdl_width='6em',fld_width='100%',row_height='3ex')
        fb.textbox(value='^.firstname',lbl='!!First name',validate_notnull=True,
                                                    validate_case='c',validate_len='2:')
        fb.textbox(value='^.lastname',lbl='!!Last name',validate_notnull=True,
                                                    validate_case='c',validate_len='2:')
        fb.textbox(value='^.email',lbl='!!Email',validate_notnull=True)
        fb.textbox(value='^.username',lbl='!!Username',validate_notnull=True,
                                    validate_nodup='adm.user.username',validate_len='4:')
        fb.checkbox(value='^.newsletter',lbl='!![en]Subscribe to newsletter')
        fb.div(width='100%',position='relative',row_hidden=False).button('!!Send',
                action='SET creating_new_user = true;',position='absolute',right='-5px',top='8px')