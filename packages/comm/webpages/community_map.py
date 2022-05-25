# -*- coding: utf-8 -*-
from gnr.core.gnrbag import Bag
class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        bc = root.borderContainer(margin='5px', datapath='main')
        map_cp = bc.contentPane(region='left', width='50%').GoogleMap( 
                        height='100%',
                        map_type='roadmap',
                        centerMarker=True,
                        nodeId='maps',
                        autoFit=True)                     
        th_dev = bc.contentPane(region='center', margin='2px').plainTableHandler(
                        nodeId='developers',
                        table='comm.developer', 
                        viewResource='ViewMap', 
                        view_store_onStart=True)
        bc.dataController(""" 
                            if(!m.map){
                                        return;
                                    }
                            m.gnr.clearMarkers(m);
                            var that = this;
                            store.forEach(function(n){
                                // console.log(n);
                                m.gnr.setMarker(m, n.attr._pkey, n.attr.position, {title:n.attr.username, 
                                                                                    onClick:function(marker_name, e){
                                                                                        //  console.log("single",marker_name,e);
                                                                                         grid.setSelectedId(marker_name);
                                                                                            },
                                                                                   // labelContent: n.attr.username,
                                                                                   // labelAnchor: new google.maps.Point(15, 0),
                                                                                   // labelClass: "markerlabel" // the CSS class for the label
                                                                                    }
                                                );
                            }, 'static');
                         """,
                            m=map_cp,
                            store='^#developers.view.store',
                            grid=th_dev.view.grid.js_widget,
                            _delay=100)