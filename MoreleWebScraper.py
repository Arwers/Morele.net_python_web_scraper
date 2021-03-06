"""
@author: Marcin Fortuna
@usage: web scraping for morele.net site
more info in readme
"""

from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup

# links to all pages
links = ['https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/1/?q=iphone',
         'https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/2/?q=iphone',
         'https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/3/?q=iphone',
         'https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/4/?q=iphone',
         'https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/5/?q=iphone',
         'https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/,,,,,,,,0,,,,/6/?q=iphone]', ]

# making CSV doc
filename = "iphoneraw.csv"  # name of the file
f = open(filename, "w")
# headers for each column
headers = "product_name, price(PLN), camera(Mpix), ram(GB), storage(GB), diagonal(inch), waterproof\n"
f.write(headers)

# opening up connection, grabbing the page
for link in links:
    my_url = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # grab each product
    cat_product = page_soup.findAll("div", {"class": "cat-product-inside"})

    container = cat_product[0]

    # loop checking every single model of phones
    for container in cat_product:
        # name of the product
        name = container.h2.a["title"]

        # price
        price_raw = container.find("div", {"class": "price-new"})
        price = price_raw.text

        # features contains lots of features below
        features = container.findAll("div", {"cat-product-feature"})

        # camera resolution in mpix
        temp_camera = features[0].text.split()
        camera = temp_camera[2]

        # ram memory in GB
        temp_ram = features[1].text.split()
        ram = temp_ram[2]

        # storage in GB
        temp_storage = features[2].text.split()
        storage = temp_storage[2]

        # screen diagonal
        temp_diagonal = features[3].text.split()
        diagonal = temp_diagonal[2]

        # IP rating
        temp_waterproof = features[4].text.split()
        waterproof = temp_waterproof[1]

        # adding row with phone features
        f.write(name + "," + price.replace(',', '.') + "," + camera + "," + ram + "," + storage + "," + diagonal +
                "," + waterproof + "\n")

# closing doc to check the doc in folder
f.close()
