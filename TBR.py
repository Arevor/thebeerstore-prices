from bs4 import BeautifulSoup
import sqlite3
import argparse
import re
import logging



class BeerContainer:
    def __init__(self, htmlpage, container_type):
        """
        Holds data for a type of container for a beer
        :param shtmlpage:  html file to be read
        :param container_type: 'can, 'bottle', or 'keg'
        """
        self.type = container_type
        self.rows = []
        try:
            self.soup = BeautifulSoup(open(htmlpage))
        except IOError:
            self.soup = 0
            return None

    def get_html_table(self):
        """
        :return: text for HTML table on BeerContainer's htmlpage
        """""
        table_tag = 'brand-pricing-wrapper brand-pricing-wrapper-'+self.type
        if self.soup:
            try:
                beer_table = self.soup.findAll("div", {"class": table_tag})
                if len(beer_table):
                    return beer_table[0]
            except IOError:
                return False

    def get_html_title(self):
        """
        :return: full name of product displayed for webpage
        """""
        if self.soup:
            try:
                beer_name = self.soup.find("h1", {"class": "page-title"}).contents[0]
                return beer_name
            except IOError:
                return False

    def get_brewery_info(self):
        """
        Parses the webpage html to find information
        :return: strings for beer category, abv, and brewery name
        """
        if self.soup:
            category = self.soup.find("dt", text="Category:").findNext("dd").contents[0]
            abv = self.soup.find(
                "dt", text="Alcohol Content (ABV):").findNext("dd").contents[0]
            brewery = self.soup.find("dt", text="Brewer:").findNext("dd").contents[0]
            return  category, abv, brewery
        else:
            return False


class Beer:
    def __init__(self, htmlpage):
        self.htmlpage = htmlpage
        self.Cans = BeerContainer(self.htmlpage, 'can')
        self.Bottles = BeerContainer(self.htmlpage, 'bottle')
        self.Kegs = BeerContainer(self.htmlpage, 'keg')

    def get_rawdata(self, BeerContainer):
        """ grabs the text contained inside the HTML table data tags
        :param BeerContainer: to have rows populated
        :return: list of row text, list of row prices
        """
        soup = BeerContainer.get_html_table()
        try:
            num_rows = len(soup.find_all('tr'))
        except AttributeError:
            return 0
        vars = []  # holds text for quantity, can or bottle, and size.
        price = []
        for i in range(0, (num_rows*3)-3, 3):
            col = soup.find_all('td')
            vars.append(col[i].contents[0])
            try:
                data = col[i+1].string.strip()
                price.append(data)
            except AttributeError:  # if there is a sale
                data = col[i+1].contents[1].contents[0]
                price.append(data)
        return vars, price

    def parse_prices(self, price_data):
        """
        :param price_data: list of prices with '$'
        :return: list of floats with $ removed
        """
        p_out = []
        for x in range(0, len(price_data)):
            out = u''.join((price_data[x])).encode('utf-8').strip()
            p_out.extend(re.findall('\d+\.\d+', out))  # extract pri
        return map(float, p_out)

    def parse_tabletext(self, variant_data):
        """
        :param variant_data: list of form [u'6  \xd7  Bottle 341\xa0ml', ...]
        :return: list of quantities, list of sizes
        """
        temp = []  # used to process quantities / sizes
        sizes = []
        quantities = []

        for x in range(0, len(variant_data)):
            out = u''.join((variant_data[x])).encode('utf-8').strip()
            temp.append(re.findall('\d+', out))  # append all digits

        for x in range(0, len(temp)):
            quantities.append(temp[x][0])
            sizes.append(temp[x][1])
        if len(quantities) == len(sizes):
            return map(int, quantities), map(int, sizes)
        else:
            return 'error paring variants'

    def get_cans(self):
        try:
            sizes, prices = self.get_rawdata(self.Cans)
            sizes, quantities= self.parse_tabletext(sizes)
            prices = self.parse_prices(prices)
            return [sizes, quantities, prices]
        except TypeError:
            return False

    def get_bottles(self):
        try:
            sizes, prices = self.get_rawdata(self.Bottles)
            sizes, quantities= self.parse_tabletext(sizes)
            prices = self.parse_prices(prices)
            return [sizes, quantities, prices]
        except TypeError:
            return False

    def get_kegs(self):
        try:
            sizes, prices = self.get_rawdata(self.Kegs)
            sizes, quantities= self.parse_tabletext(sizes)
            prices = self.parse_prices(prices)
            return [sizes, quantities, prices]
        except TypeError:
            return False


    # def format_rows(self,  prices, quantities, sizes):
    #     if len(prices) == len(quantities) == len(sizes):
    #         rows, cols = len(prices), 3
    #         product_data = [[0 for x in range(cols)] for y in range(rows)]
    #         for x in range(0, len(prices)):
    #             product_data[x][0] = prices[x]
    #             product_data[x][1] = quantities[x]
    #             product_data[x][2] = sizes[x]
    #         return product_data
    #     else:
    #         return 'error formatting rows'


class BeerRetriever:
    def __init__(self, db_file, htmlpage, log_file):
        self.my_beer = Beer(htmlpage)
        self.my_db = Database(db_file)
        self.name = self.my_beer.Kegs.get_html_title()

        self.htmlpage = htmlpage
        logging.basicConfig(filename=log_file,
                            filemode='a',
                            format='%(asctime)s:%(msecs)d %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        logging.info('--------------------------------------------------')
        logging.info('Starting import of ' + self.htmlpage)


    def retreieve_info(self):
        vals = self.my_beer.Kegs.get_brewery_info()
        self.my_db.insert_brewery(self.name, vals[0], vals[1], vals[2])

    def retrieve_cans(self):
        cans = self.my_beer.get_cans()
        self.my_db.insert_container(self.name, 'Can', cans)

    def retrieve_bottles(self):
        bottles = self.my_beer.get_bottles()
        self.my_db.insert_container(self.name, 'Bottle', bottles)

    def retrieve_kegs(self):
        keg = self.my_beer.get_kegs()
        self.my_db.insert_container(self.name, 'Keg', keg)

    def retrieve(self):
        self.retreieve_info()
        self.retrieve_cans()
        self.retrieve_bottles()
        self.retrieve_kegs()


class Database:

    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.c = self.con.cursor()



    def insert_brewery(self, beer, category, abv, brewery):
        vals = (beer, category, abv, brewery)
        try:
            self.c.execute('''INSERT INTO breweries values(?, ?, ?, ?)''', vals)
            self.con.commit()
            logging.info(str(vals) + "added to breweries table")
        except sqlite3.IntegrityError:
            logging.info(str(vals) + "NOT added to breweries table-- already exists")

    def insert_container(self, beer, container_type, data):
        if isinstance(data, bool):
            return 0
        data = map(list, zip(*data))
        if isinstance(data, list):
            for i in range(0, len(data)):

                data[i].insert(0, beer)
                data[i].append(container_type)
                data[i].append(hash(str(data[i])))
                try:
                    self.c.execute('''INSERT INTO products values(?, ?, ?, ?,
                                      ?, ?, CURRENT_TIMESTAMP)''', data[i])
                    self.con.commit()
                except sqlite3.IntegrityError:
                   pass
        else:
           print 'Not Available'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db_file", help="database file for sqlite3")
    parser.add_argument("htmlpage", help="page of prices to scan")
    parser.add_argument("log_file", help="output log file")
    args = parser.parse_args()

    buddy = BeerRetriever(args.db_file, args.htmlpage, args.log_file)

    buddy.retrieve()










