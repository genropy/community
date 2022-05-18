from gnr.web.gnrbaseclasses import BaseComponent


class LoginComponent(BaseComponent):
            
    def onUserSelected(self, avatar, data):
        developer_id = self.db.table("comm.developer").readColumns(where='$user_id=:u_id',u_id=avatar.user_id, columns="$id")
        data.setItem("developer_id", developer_id)