from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup


def price_formating(value):
    price_list = value.text.split()
    x = price_list[0] + price_list[1]
    finalprice = []
    for i in x:
        if i == ",":
            finalprice.append(".")
            continue
        finalprice.append(i)
    return "".join(finalprice)


def diagonal_formating(value):
    finaldiagonal = []
    for i in range(0, (len(value)-1)):
        finaldiagonal.append(value[i])

    return "".join(finaldiagonal)


# opening up connection, grabbing the page
my_url = Request('https://www.morele.net/telefony/telefony-smartfony-krotkofalowki/smartfony-280/?q=iphone',
                 headers={'User-Agent': 'Mozilla/5.0'})
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grab each product
cat_product = page_soup.findAll("div", {"class": "cat-product-inside"})

container = cat_product[0]

filename = "iphones.csv"
f = open(filename, "w")
headers = "product_name, price(PLN), camera(Mpix), ram(GB), storage(GB), diagonal(inch), waterproof\n"
f.write(headers)
for container in cat_product:
    name = container.h2.a["title"]

    price_raw = container.find("div", {"class": "price-new"})
    price = price_formating(price_raw)

    features = container.findAll("div", {"cat-product-feature"})

    temp_camera = features[0].text.split()
    camera = temp_camera[2]

    temp_ram = features[1].text.split()
    ram = temp_ram[2]

    temp_storage = features[2].text.split()
    storage = temp_storage[2]

    temp_diagonal = features[3].text.split()
    diagonal_raw = temp_diagonal[2]
    diagonal = diagonal_formating(str(diagonal_raw))

    temp_waterproof = features[4].text.split()
    waterproof = temp_waterproof[1]

    f.write(name + "," + price + "," + camera + "," + ram + "," + storage + "," + diagonal + "," + waterproof + "\n")

f.close()
