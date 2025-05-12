class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler'

    def main(self, root, **kwargs):
        kw = {'initialView':'dayGridMonth',
              'headerToolbar': {
                    'center': 'addEventButton'
              },
            'customButtons': {
                'addEventButton': {
                'text': 'add event...'}
        }}
        root.contentPane(region='center', datapath='main').fullCalendar(table='social.post', condition='$id IS NOT NULL',
                                                                        box_margin='40px',box_max_width='1100px', **kw)
        