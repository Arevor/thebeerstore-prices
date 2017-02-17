import unittest
from TBR import BeerContainer, Beer, BeerRetriever

# TODO clean up unit testing
class TestBeerContainer(unittest.TestCase):
    # html_src/TST-carlsberg for 'sales'
    # html_scr/TST-amsterdamn-b... for 'new'
    # html_src/TST-budweiser for alternate cans
    def setUp(self):
        self.carlsbergA = BeerContainer('test_html/TST-carlsberg', 'can')
        self.carlsbergB = BeerContainer('test_html/TST-idontexist', 'can')
        self.carlsbergC = BeerContainer('test_html/TST-idontexist', 'buckets')
        self.carlsbergD = BeerContainer('test_html/TST-carlsberg', 'bottle')
        self.budweiser = BeerContainer('test_html/TST-budweiser', 'can')
        self.pbr = BeerContainer('html_src/pabst-blue-ribbon', 'can')


    def test_add_row(self):
        out_list = ['Budweiser', 2.50, 1, 473] # with empty list
        self.assertEqual(self.budweiser.add_row(2.50, 1, 473), out_list)
        out_list = [[123,], ['Budweiser', 2.50, 1, 473]] # Nth entry
        self.assertEqual(self.budweiser.add_row(2.50, 1, 473), out_list[1])

    def test_get_html_table(self):
        self.assertTrue(self.carlsbergA.get_html_table())
        self.assertFalse(self.carlsbergB.get_html_table())
        self.assertFalse(self.carlsbergC.get_html_table())
        self.assertTrue(self.carlsbergD.get_html_table())

    def test_get_html_title(self):
        # valid
        self.assertEquals(self.budweiser.get_html_title(), "Budweiser")
        self.assertEquals(self.pbr.get_html_title(), "Pabst Blue Ribbon")
        self.assertEquals(self.budweiser.get_html_title(), "Budweiser")
        # invalid
        self.assertFalse(self.carlsbergB.get_html_title())
        self.assertFalse(self.carlsbergC.get_html_title())

    def test_get_brewery_info(self):
        data = ('Premium', '5.0%', 'Labatt')
        self.assertEquals(self.budweiser.get_brewery_info(), data)


        data = ('Value', '4.9%', 'Sleeman Brewing')
        self.assertEquals(self.pbr.get_brewery_info(), data)

        self.assertFalse(self.carlsbergC.get_brewery_info(), data)

class TestBeer(unittest.TestCase):

    def setUp(self):
        self.bud = Beer('test_html/TST-budweiser')
        self.carl = Beer('test_html/TST-carlsberg')
        self.PBR = Beer('html_src/pabst-blue-ribbon-59')
        self.AM = Beer('test_html/TST-amsterdam-boneshaker-ipa')
        self.cam = Beer('html_src/camerons-lager')
        self.can = Beer('html_src/canadian')


        self.carlsbergA = BeerContainer('test_html/TST-carlsberg', 'can')
        self.carlsbergB = BeerContainer('test_html/TST-idontexist', 'can')
        self.carlsbergC = BeerContainer('test_html/TST-idontexist', 'buckets')
        self.carlsbergD = BeerContainer('test_html/TST-carlsberg', 'bottle')
        self.budweiser = BeerContainer('test_html/TST-budweiser', 'can')
        self.pbr = BeerContainer('html_src/pabst-blue-ribbon', 'can')
        self.pbr2 = BeerContainer('html_src/pabst-blue-ribbon', 'bottle')
        self.am = BeerContainer('test_html/TST-amsterdam-boneshaker-ipa', 'can')
        self.amB = BeerContainer('test_html/TST-amsterdam-boneshaker-ipa', 'bottle')
        self.CAM = BeerContainer('html_src/camerons-lager', 'can')
        self.CAN = BeerContainer('html_src/canadian', 'bottle')

    def test_gather_raw_rowdata(self):
        # test PBR cans
        pbr_price =  [u'$2.05', u'$4.00', u'$11.50', u'$20.95', u'$22.95',
                      u'$30.50', u'$37.95', u'$45.75', u'$59.95', u'$89.95']
        pbr_tabletext =  [u'1  \xd7  Can 473\xa0ml', u'2  \xd7  Can 473\xa0ml',
                          u'6  \xd7  Can 473\xa0ml', u'12  \xd7  Can 355\xa0ml',
                          u'12  \xd7  Can 473\xa0ml', u'20  \xd7  Can 355\xa0ml',
                          u'24  \xd7  Can 355\xa0ml', u'24  \xd7  Can 473\xa0ml',
                          u'40  \xd7  Can 355\xa0ml', u'60  \xd7  Can 355\xa0ml']
        self.assertEquals(self.PBR.gather_raw_rowdata(self.pbr),
                          (pbr_tabletext, pbr_price))
        # 1 sale item
        carl_price = [u' on sale $2.40', u'$13.10', u'$45.95', u'$53.95']
        carl_tabletext =[u'1  \xd7  Can 500\xa0ml', u'6  \xd7  Can 330\xa0ml',
                         u'24  \xd7  Can 330\xa0ml', u'24  \xd7  Can 500\xa0ml']
        self.assertEquals(self.carl.gather_raw_rowdata(self.carlsbergA),
                          (carl_tabletext, carl_price))
        am_table_text =  [u'1  \xd7  Can 473\xa0ml', u'8  \xd7  Can 473\xa0ml',
        # 2 'NEW' tags
                          u'16  \xd7  Can 473\xa0ml', u'24  \xd7  Can 473\xa0ml']
        am_price = [u'$3.15', u'$24.50', u'$48.00', u'$69.00']
        self.assertEquals(self.AM.gather_raw_rowdata(self.am),
        (am_table_text, am_price))


        cam_table_text = [u'1  \xd7  Can 473\xa0ml', u'4  \xd7  Can 473\xa0ml',
                          u'6  \xd7  Can 473\xa0ml', u'24  \xd7  Can 473\xa0ml']
        cam_price = [u' on sale $2.85', u'$11.95', u'$16.95', u' on sale $59.95']
        self.assertEquals(self.cam.gather_raw_rowdata(self.CAM),
                          (cam_table_text, cam_price))

        can_table_text = [u'6  \xd7  Bottle 341\xa0ml', u'12  \xd7  Bottle 341\xa0ml',
                          u'12  \xd7  Bottle 710\xa0ml', u'15  \xd7  Bottle 341\xa0ml',
                          u'18  \xd7  Bottle 341\xa0ml', u'24  \xd7  Bottle 341\xa0ml',
                          u'28  \xd7  Bottle 341\xa0ml', u'30  \xd7  Bottle 341\xa0ml',
                          u'36  \xd7  Bottle 341\xa0ml']
        can_price =  [u'$11.95', u'$21.95', u'$42.95', u'$26.95', u'$31.95',
                      u'$38.95', u'$40.95', u'$45.95', u' on sale $50.00']
        self.assertEquals(self.can.gather_raw_rowdata(self.CAN),
                          (can_table_text, can_price))

        # TODO page that has alunimum can under the can section

    def test_parse_prices(self):
        data1 = ['$1.05', '$2.03', '$3.03']
        data2 = ['$asdf', '$3.0', 'no']
        data3 = [u'$2.05', u'$4.00', u'$11.50']

        self.assertEquals(self.PBR.parse_prices(data1), [1.05, 2.03, 3.03])
        self.assertEquals(self.PBR.parse_prices(data2), [3.00])
        self.assertEquals(self.PBR.parse_prices(data3), [2.05, 4.00, 11.50])


    def test_parse_tabletext(self):

        pbr_text = [u'1  \xd7  Can 473\xa0ml', u'2  \xd7  Can 473\xa0ml',
                    u'6  \xd7  Can 473\xa0ml', u'12  \xd7  Can 355\xa0ml',
                    u'12  \xd7  Can 473\xa0ml', u'20  \xd7  Can 355\xa0ml',
                    u'24  \xd7  Can 355\xa0ml', u'24  \xd7  Can 473\xa0ml',
                    u'40  \xd7  Can 355\xa0ml', u'60  \xd7  Can 355\xa0ml']
        pbr_qty_out = [1, 2, 6, 12, 12, 20, 24, 24, 40, 60]
        pbr_size_out = [473, 473, 473, 355, 473, 355, 355, 473, 355, 355]
        self.assertEquals(self.PBR.parse_tabletext(pbr_text),
                          (pbr_qty_out, pbr_size_out))

    def test_get_cans(self):
        pbr_cans = [[1, 2, 4, 6, 6, 12, 12, 24, 24],
                    [473, 473, 473, 355, 473, 355, 473, 355, 473],
        [2.15, 4.25, 8.45, 9.5, 12.25, 19.0, 24.45, 37.95, 48.9]]
        self.assertEquals(self.PBR.get_cans(), pbr_cans)

        am_cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
        self.assertEquals(self.AM.get_cans(), am_cans)

        am_cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
        self.assertEquals(self.AM.get_cans(), am_cans)

    def test_get_bottles(self):
        # invalid
        pbr_bots = [[1, 2, 4, 6, 6, 12, 12, 24, 24],
                    [473, 473, 473, 355, 473, 355, 473, 355, 473],
        [2.15, 4.25, 8.45, 9.5, 12.25, 19.0, 24.45, 37.95, 48.9]]
        self.assertFalse(self.PBR.get_bottles())

        # valid
        self.assertFalse(self.PBR.get_bottles())

        am_bots = [[6, 12, 24], [355, 355, 355], [13.25, 27.00, 52.95]]
        self.assertEquals(self.AM.get_bottles(), am_bots)

    def test_get_kegs(self):
        pass

class TestBeerRetriever(unittest.TestCase):

    def setUp(self):
        self.amsterdam = BeerRetriever('test_html/TST-amsterdam-boneshaker-ipa')


    def test_retrieve_cans(self):
        cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
        self.assertEquals(self.amsterdam.retrieve_cans(), cans)

    def test_retrieve_bottles(self):
        bottles = [[6, 12, 24], [355, 355, 355], [13.25, 27.00, 52.95]]
        self.assertEquals(self.amsterdam.retrieve_bottles(), bottles)

    def test_retrieve_kegs(self):
        self.assertFalse(self.amsterdam.retrieve_kegs())