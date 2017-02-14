from bs4 import BeautifulSoup
import sqlite3
import argparse
import re


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

    def add_row(self, price, quantity, size):
        """ adds a row to BeerContainer
        :param price: price for given quantity
        :param quantity:
        :param size: size of container. 500ml, 473ml, 355ml, etc.
        :return: last entry in list
        """""
        self.rows.append([self.get_html_title(), price, quantity, size])
        return self.rows[-1]

    def get_rows(self):
        """
        :return: all of the rows in this BeerContainer
        """""
        return self.rows

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
        self.Cans = BeerContainer(htmlpage, 'can')
        self.Bottles = BeerContainer(htmlpage, 'bottle')
        self.Kegs = BeerContainer(htmlpage, 'keg')

    def gather_raw_rowdata(self, BeerContainer):
        """ grabs the text contained inside the HTML table data tags
        :param BeerContainer: to have rows populated
        :return: list of row text, list of row prices
        """
        soup = BeerContainer.get_html_table()
        num_rows = len(soup.find_all('tr'))
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