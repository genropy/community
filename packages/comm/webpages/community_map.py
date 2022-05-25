# -*- coding: utf-8 -*-
            
class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        bc = root.borderContainer(margin='5px', datapath='main')
        bc.contentPane(region='top', height='50%').GoogleMap( 
                    height='100%',
                    map_center="^.comm_developer.view.store.r_0?position",
                    map_type='roadmap',
                    map_zoom=15,
                    centerMarker=True)                      
        bc.contentPane(region='center').plainTableHandler(table='comm.developer', 
                    viewResource='ViewMap', view_store_onStart=True)