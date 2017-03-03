# To populate a database with Prices:

* retrieve all HTML sources with wget

```BASH
wget -r -nH --cut-dirs=2 --no-parent --reject="index.html*" http://www.thebeerstore.ca/beers/ 
```
* create sqlite DB with db_create.sql

* Run all of the HTML through TBR.py

```BASH
for f in html_src/*; do echo "File: ${f}"; python TBR.py ${f} 2>/dev/null; echo  ""; done
```
* write SQL to get what you what from the DB

# Dependencies 

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* Python 2.7
