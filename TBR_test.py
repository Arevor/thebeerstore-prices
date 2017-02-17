import unittest
from TBR import BeerContainer, Beer, BeerRetriever

# TODO clean up unit testing
class TestBeerContainer(unittest.TestCase):
    # html_scr/TEST-amsterdamn-b... for 'new'
    # html_src/TEST-budweiser for alternate cans
    # html_src/TEST-carlsberg for 'sales'
    # html_src/TEST-pabst-blue-ribbon-59 because
    def setUp(self):
        amsterdam_src = 'test_html/test-amsterdam-boneshaker-ipa'
        budweiser_src = 'test_html/test-budweiser'
        carlsberg_src = 'test_html/test-carlsberg'
        pbr59_src = 'test_html/test-pabst-blue-ribbon-59'

        # valid
        self.amsterCan = BeerContainer(amsterdam_src, 'can')
        self.budKeg = BeerContainer(budweiser_src, 'keg')
        self.budCan = BeerContainer(budweiser_src, 'can')
        self.carlCan = BeerContainer(carlsberg_src, 'can')
        self.carlBot = BeerContainer(carlsberg_src, 'bottle')
        self.pbrCan = BeerContainer(pbr59_src, 'can')

        # invalid
        self.carlsbergA = BeerContainer('test_html/TST-carlsberg', 'can')
        self.carlsbergB = BeerContainer('test_html/TST-idontexist', 'can')
        self.carlsbergC = BeerContainer('test_html/TST-idontexist', 'buckets')
        self.pbrA = BeerContainer(pbr59_src, 'asdf')



    def test_get_html_table(self):
        # valid
        self.assertTrue(self.amsterCan.get_html_table())
        self.assertTrue(self.budKeg.get_html_table())
        self.assertTrue(self.carlCan.get_html_table())
        self.assertTrue(self.carlBot.get_html_table())

        # invalid
        self.assertFalse(self.carlsbergA.get_html_table())
        self.assertFalse(self.carlsbergB.get_html_table())
        self.assertFalse(self.carlsbergC.get_html_table())
        self.assertFalse(self.pbrA.get_html_table())

    def test_get_html_title(self):
        # valid
        self.assertEquals(self.amsterCan.get_html_title(), "Amsterdam Boneshaker IPA ")
        self.assertEquals(self.pbrCan.get_html_title(), "Pabst Blue Ribbon 5.9")
        self.assertEquals(self.budKeg.get_html_title(), "Budweiser")
        # invalid
        self.assertFalse(self.carlsbergA.get_html_title())
        self.assertFalse(self.carlsbergB.get_html_title())
        self.assertFalse(self.carlsbergC.get_html_title())

    def test_get_brewery_info(self):
        # valid
        data = ('Premium', '5.0%', 'Labatt')
        self.assertEquals(self.budKeg.get_brewery_info(), data)

        data = ('Premium', '5.9%', 'Sleeman Brewing')
        self.assertEquals(self.pbrCan.get_brewery_info(), data)

        # invalid
        self.assertFalse(self.carlsbergA.get_brewery_info(), data)
        self.assertFalse(self.carlsbergB.get_brewery_info(), data)
        self.assertFalse(self.carlsbergC.get_brewery_info(), data)

class TestBeer(unittest.TestCase):

    def setUp(self):
        amsterdam_src = 'test_html/test-amsterdam-boneshaker-ipa'
        budweiser_src = 'test_html/test-budweiser'
        carlsberg_src = 'test_html/test-carlsberg'
        pbr59_src = 'test_html/test-pabst-blue-ribbon-59'

        # Beer Containers
        self.amsterCan = BeerContainer(amsterdam_src, 'can')
        self.budKeg = BeerContainer(budweiser_src, 'keg')
        self.budCan = BeerContainer(budweiser_src, 'can')
        self.carlCan = BeerContainer(carlsberg_src, 'can')
        self.carlBot = BeerContainer(carlsberg_src, 'bottle')
        self.pbrCan = BeerContainer(pbr59_src, 'can')


        # Beers
        self.bud = Beer(budweiser_src)
        self.carl = Beer(carlsberg_src)
        self.PBR = Beer(pbr59_src)
        self.AM = Beer(amsterdam_src)
        self.cam = Beer('html_src/camerons-lager')
        self.can = Beer('html_src/canadian')


        self.carlsbergA = BeerContainer('test_html/test-carlsberg', 'can')
        self.carlsbergB = BeerContainer('test_html/test-idontexist', 'can')
        self.carlsbergC = BeerContainer('test_html/test-idontexist', 'buckets')
        self.carlsbergD = BeerContainer('test_html/test-carlsberg', 'bottle')
        self.budweiser = BeerContainer('test_html/test-budweiser', 'can')
        self.pbr = BeerContainer('html_src/pabst-blue-ribbon', 'can')
        self.pbr2 = BeerContainer('html_src/pabst-blue-ribbon', 'bottle')
        self.am = BeerContainer('test_html/test-amsterdam-boneshaker-ipa', 'can')
        self.amB = BeerContainer('test_html/test-amsterdam-boneshaker-ipa', 'bottle')
        self.CAM = BeerContainer('html_src/camerons-lager', 'can')
        self.CAN = BeerContainer('html_src/canadian', 'bottle')

    def test_gather_raw_rowdata(self):
        # test PBR cans
        price =  [u'$2.05', u'$4.00', u'$11.50', u'$20.95', u'$22.95',
                  u'$30.50', u'$37.95', u'$45.75', u'$59.95', u'$89.95']
        text =  [u'1  \xd7  Can 473\xa0ml', u'2  \xd7  Can 473\xa0ml',
                 u'6  \xd7  Can 473\xa0ml', u'12  \xd7  Can 355\xa0ml',
                 u'12  \xd7  Can 473\xa0ml', u'20  \xd7  Can 355\xa0ml',
                 u'24  \xd7  Can 355\xa0ml', u'24  \xd7  Can 473\xa0ml',
                 u'40  \xd7  Can 355\xa0ml', u'60  \xd7  Can 355\xa0ml']
        self.assertEquals(self.PBR.get_rawdata(self.pbr), (text, price))

        # 1 sale item
        price = [u' on sale $2.40', u'$13.10', u'$45.95', u'$53.95']
        text = [u'1  \xd7  Can 500\xa0ml', u'6  \xd7  Can 330\xa0ml',
                u'24  \xd7  Can 330\xa0ml', u'24  \xd7  Can 500\xa0ml']
        self.assertEquals(self.carl.get_rawdata(self.carlCan), (text, price))

        # 2 'NEW' tags
        text =  [u'1  \xd7  Can 473\xa0ml', u'8  \xd7  Can 473\xa0ml',
                 u'16  \xd7  Can 473\xa0ml', u'24  \xd7  Can 473\xa0ml']
        price = [u'$3.15', u'$24.50', u'$48.00', u'$69.00']
        self.assertEquals(self.AM.get_rawdata(self.am), (text, price))


        text = [u'1  \xd7  Can 473\xa0ml', u'4  \xd7  Can 473\xa0ml',
                u'6  \xd7  Can 473\xa0ml', u'24  \xd7  Can 473\xa0ml']
        price = [u' on sale $2.85', u'$11.95', u'$16.95', u' on sale $59.95']
        self.assertEquals(self.cam.get_rawdata(self.CAM), (text, price))

        text = [u'6  \xd7  Bottle 341\xa0ml', u'12  \xd7  Bottle 341\xa0ml',
                u'12  \xd7  Bottle 710\xa0ml', u'15  \xd7  Bottle 341\xa0ml',
                u'18  \xd7  Bottle 341\xa0ml', u'24  \xd7  Bottle 341\xa0ml',
                u'28  \xd7  Bottle 341\xa0ml', u'30  \xd7  Bottle 341\xa0ml',
                u'36  \xd7  Bottle 341\xa0ml']
        price =  [u'$11.95', u'$21.95', u'$42.95', u'$26.95', u'$31.95',
                  u'$38.95', u'$40.95', u'$45.95', u' on sale $50.00']
        self.assertEquals(self.can.get_rawdata(self.CAN), (text,price))

        # TODO page that has alunimum can under the can section

    def test_parse_prices(self):
        data1 = ['$1.05', '$2.03', '$3.03']
        data2 = ['$asdf', '$3.0', 'no']
        data3 = [u'$2.05', u'$4.00', u'$11.50']

        self.assertEquals(self.PBR.parse_prices(data1), [1.05, 2.03, 3.03])
        self.assertEquals(self.PBR.parse_prices(data2), [3.00])
        self.assertEquals(self.PBR.parse_prices(data3), [2.05, 4.00, 11.50])


    def test_parse_tabletext(self):

        text = [u'1  \xd7  Can 473\xa0ml', u'2  \xd7  Can 473\xa0ml',
                u'6  \xd7  Can 473\xa0ml', u'12  \xd7  Can 355\xa0ml',
                u'12  \xd7  Can 473\xa0ml', u'20  \xd7  Can 355\xa0ml',
                u'24  \xd7  Can 355\xa0ml', u'24  \xd7  Can 473\xa0ml',
                u'40  \xd7  Can 355\xa0ml', u'60  \xd7  Can 355\xa0ml']
        qty = [1, 2, 6, 12, 12, 20, 24, 24, 40, 60]
        size = [473, 473, 473, 355, 473, 355, 355, 473, 355, 355]
        self.assertEquals(self.PBR.parse_tabletext(text), (qty, size))

    def test_get_cans(self):
        cans = [[1, 2, 4, 6, 6, 12, 12, 24, 24],
                [473, 473, 473, 355, 473, 355, 473, 355, 473],
        [2.15, 4.25, 8.45, 9.5, 12.25, 19.0, 24.45, 37.95, 48.9]]
        self.assertEquals(self.PBR.get_cans(), cans)

        cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
        self.assertEquals(self.AM.get_cans(), cans)

        cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
        self.assertEquals(self.AM.get_cans(), cans)

    def test_get_bottles(self):
        # invalid
        bots = [[1, 2, 4, 6, 6, 12, 12, 24, 24],
                [473, 473, 473, 355, 473, 355, 473, 355, 473],
        [2.15, 4.25, 8.45, 9.5, 12.25, 19.0, 24.45, 37.95, 48.9]]
        self.assertFalse(self.PBR.get_bottles())

        # valid
        self.assertFalse(self.PBR.get_bottles())

        bots = [[6, 12, 24], [355, 355, 355], [13.25, 27.00, 52.95]]
        self.assertEquals(self.AM.get_bottles(), bots)

    def test_get_kegs(self):
        pass

# class TestBeerRetriever(unittest.TestCase):

    # def setUp(self):
    #     self.amsterdam = BeerRetriever('test_html/test-amsterdam-boneshaker-ipa')


    # def test_retrieve_cans(self):
    #     cans = [[1, 8, 16, 24], [473, 473, 473, 473], [3.15, 24.5, 48.0, 69.0]]
    #     self.assertEquals(self.amsterdam.retrieve_cans(), cans)

    # def test_retrieve_bottles(self):
    #     bottles = [[6, 12, 24], [355, 355, 355], [13.25, 27.00, 52.95]]
    #     self.assertEquals(self.amsterdam.retrieve_bottles(), bottles)

    # def test_retrieve_kegs(self):
    #     self.assertFalse(self.amsterdam.retrieve_kegs())