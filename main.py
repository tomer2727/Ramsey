from ShufersalScraper import ShufersalScraper
from Product import Product
product_to_search = "עגבניה"
quantity = 10

#initialize the scraper
scraper = ShufersalScraper()

#get the products
products_htmls = scraper.search_product(product_to_search, quantity)

#print the products
for product_html in products_htmls:
    product = Product(product_html)
    print(product)
