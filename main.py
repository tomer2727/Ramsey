import os
import time
import json
from ShufersalScraper import ShufersalScraper
from Product import Product
from agent import generate_search_queries
import hashlib

# Set this flag to True to use cache, False to always recompute
USE_CACHE = False
CACHE_FILE = 'cache.json'
CACHE_EXPIRY_SECONDS = 30 * 60  # 30 minutes

user_prefences="""
מעדיף תוצרת כחול לבן
מעדיף מוצרי פרימיום
מעדיף מוצרים ארוזים על מוצרים בתפזורת
מעדיף את חברת אווטלי במשקה שיבולת שועל
"""
shopping_list = ["חלב שיבולת שועל אווטלי", "2 קילו עגבניות מגי",  "1 קילו פסטה פנה", "1 קילו שמן זית כתית מעולה"]

def get_cache_key(shopping_list):
    # Use a hash of the shopping list as the cache key
    return hashlib.sha256(json.dumps(shopping_list, ensure_ascii=False).encode()).hexdigest()

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        try:
            cache = json.load(f)
        except Exception:
            return None
    return cache

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)

cache = load_cache() if USE_CACHE else None
cache_key = get_cache_key(shopping_list)
now = time.time()

use_cached = False
if cache and cache_key in cache:
    entry = cache[cache_key]
    if now - entry['timestamp'] < CACHE_EXPIRY_SECONDS:
        use_cached = True
        possible_products = entry['possible_products']
        print('Loaded results from cache.')

if not use_cached:
    #initialize the scraper
    scraper = ShufersalScraper(headless=True)
    #generate search queries
    search_queries = []
    for item in shopping_list:
        search_queries.append(generate_search_queries(item))
    #get the products
    possible_products = []
    for item_specific_queries in search_queries:
        for query in item_specific_queries:
            products_htmls = scraper.search_product(query, 5)
            for product_html in products_htmls:
                product = Product(product_html)
                # Save only the parsed, LLM-ready structure
                possible_products.append({product.class_name: product.value})
    # Save to cache
    if USE_CACHE:
        if not cache:
            cache = {}
        cache[cache_key] = {
            'timestamp': now,
            'possible_products': possible_products
        }
        save_cache(cache)
        print('Saved results to cache.')

#dump the possible products to a json file well formatted
with open('possible_products.json', 'w') as f:
    json.dump(possible_products, f, indent=4, ensure_ascii=False)

