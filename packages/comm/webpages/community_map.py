# -*- coding: utf-8 -*-

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        bc = root.borderContainer(datapath='main')
        th_args = dict(region='bottom', height='50%') if self.isMobile else dict(region='right', width='50%') 
        map_cp = bc.contentPane(**th_args).GoogleMap( 
                        height='100%', width='100%',
                        map_type='roadmap',
                        centerMarker=True,
                        map_center='^gnr.user_coords',
                        nodeId='gma',
                        autoFit=True)         
        
        adminUser = self.application.checkResourcePermission('admin',self.userTags)
        th_dev = bc.contentPane(region='center').plainTableHandler(
                        nodeId='developers',
                        table='comm.developer', 
                        viewResource='ViewMap', 
                        groupable=dict(static=not adminUser),
                        configurable=adminUser,
                        view_store_onStart=True,
                        addrow=False, delrow=False,
                        grid__class='noheader'
                        )
        bc.dataController("""
                            if(!m.map){
                                        return;
                                    }
                            genro.getUserLocation();
                            m.gnr.clearMarkers(m);
                            var that = this;
                            store.forEach(function(n){
                                console.log(n);
                                m.gnr.setMarker(m, n.attr._pkey, n.attr.position, {title:n.attr.tg_username, 
                                                                                   onClick:function(marker_name, e){
                                                                                            grid.setSelectedId(marker_name); },
                                                                                    labelContent: n.attr.tg_username,
                                                                                    labelAnchor: new google.maps.Point(15, 0),
                                                                                    labelClass: "markerlabel" // the CSS class for the label
                                                                                    }
                                                );
                            }, 'static');
                            m.gnr.fitMarkers(m);""",
                            m=map_cp,
                            store='^#developers.view.store',
                            grid=th_dev.view.grid.js_widget,
                            _delay=100)