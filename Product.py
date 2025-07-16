from bs4 import BeautifulSoup
from typing import Optional, List
import re

class Product:
    def __init__(self, raw_html: str):
        self.raw_html = raw_html
        soup = BeautifulSoup(raw_html, 'html.parser')
        li = soup.find(['li']) or soup

        # Extract product ID
        self.id: Optional[str] = li.get('data-product-code')
        # Extract product name
        self.name: Optional[str] = li.get('data-product-name')
        # Extract selling method
        self.selling_method: Optional[str] = li.get('data-selling-method')
        # Extract price (main price, as string)
        self.price: Optional[str] = li.get('data-product-price')
        # Initialize fields
        self.brand: Optional[str] = None
        self.unit: Optional[str] = None
        self.unit_type: Optional[str] = None  # 'weight', 'unit', 'package', 'unknown'
        self.unit_count: Optional[int] = None
        self.price_per_unit: Optional[float] = None
        self.price_total: Optional[float] = None
        self.price_unit_label: Optional[str] = None

        # Extract brand and unit/package info
        brand_tag = li.select_one('.brand-name')
        if brand_tag:
            spans = brand_tag.find_all('span')
            if len(spans) > 1:
                self.unit = spans[0].get_text(strip=True)
                self.brand = spans[1].get_text(strip=True)
            elif spans:
                self.unit = spans[0].get_text(strip=True)
        # Standardize unit_type and extract unit_count if possible
        self.unit_type = 'unknown'
        if self.unit:
            if 'ק"ג' in self.unit or 'משקל' in self.unit:
                self.unit_type = 'weight'
            elif 'יחידה' in self.unit or 'יחידות' in self.unit:
                self.unit_type = 'unit'
            elif 'מכיל' in self.unit:
                self.unit_type = 'package'
                # Try to extract unit count
                match = re.search(r'מכיל כ?-?\s*(\d+)', self.unit)
                if match:
                    self.unit_count = int(match.group(1))
            elif 'גרם' in self.unit:
                self.unit_type = 'weight'
        # Extract priceUnit (e.g., לק"ג, ל- 1 ק"ג, ל- 100 גרם, ל- 1 יחידה)
        price_unit_tag = li.select_one('.priceUnit')
        if price_unit_tag:
            self.price_unit_label = price_unit_tag.get_text(strip=True)
        # Extract price per unit (from .pricePerUnit)
        price_per_unit_tag = li.select_one('.pricePerUnit')
        if price_per_unit_tag:
            # Try to extract the number (e.g., 8.9 ש"ח ל- 1 ק"ג)
            match = re.search(r'([\d.]+)\s*ש"ח', price_per_unit_tag.get_text())
            if match:
                self.price_per_unit = float(match.group(1))
        # Extract total price (from .price .number or .price span[itemprop="price"])
        price_number_tag = li.select_one('.price .number')
        if price_number_tag:
            try:
                self.price_total = float(price_number_tag.get_text(strip=True))
            except Exception:
                self.price_total = None
        else:
            # Try alternative price location
            price_itemprop_tag = li.select_one('.price span[itemprop="price"]')
            if price_itemprop_tag:
                try:
                    self.price_total = float(re.sub(r'[^\d.]', '', price_itemprop_tag.get_text(strip=True)))
                except Exception:
                    self.price_total = None
        # Extract stock status (improved logic: check parent class for inStock)
        self.stock_status: Optional[str] = None
        tile_div = li.select_one('.tile')
        if tile_div:
            classes = tile_div.get('class', [])
            if 'miglog-prod-inStock' in classes:
                self.stock_status = 'in_stock'
            elif 'miglog-prod-outOfStock' in classes:
                self.stock_status = 'out_of_stock'
        # Fallback: check for visible outOfStock message
        if not self.stock_status:
            stock_tag = li.select_one('.miglog-prod-outOfStock-msg')
            if stock_tag and stock_tag.get_text(strip=True):
                self.stock_status = stock_tag.get_text(strip=True)
            else:
                low_stock_tag = li.select_one('.miglog-prod-lowStock-msg')
                if low_stock_tag and low_stock_tag.get_text(strip=True):
                    self.stock_status = low_stock_tag.get_text(strip=True)
        # Extract image URL
        self.image_url: Optional[str] = None
        img_tag = li.select_one('img.pic')
        if img_tag:
            self.image_url = img_tag.get('src')
        # Extract special offers (from .promotion-section or .promotionTooltipWrapper)
        self.special_offers: Optional[str] = None
        promo_tag = li.select_one('.promotion-section strong')
        if promo_tag:
            self.special_offers = promo_tag.get_text(strip=True)
        # Extract labels (e.g., vegan, organic, etc.)
        self.labels: List[str] = []
        label_tags = li.select('.labelInner .rotateText, .labelsList .btnTooltip[aria-label]')
        for tag in label_tags:
            label = tag.get('aria-label') or tag.get_text(strip=True)
            if label:
                self.labels.append(label)

    def __repr__(self):
        return (
            f"Product(id={self.id!r}, name={self.name!r}, brand={self.brand!r}, "
            f"selling_method={self.selling_method!r}, price={self.price!r}, unit={self.unit!r}, "
            f"unit_type={self.unit_type!r}, unit_count={self.unit_count!r}, price_total={self.price_total!r}, "
            f"price_per_unit={self.price_per_unit!r}, price_unit_label={self.price_unit_label!r}, "
            f"stock_status={self.stock_status!r}, image_url={self.image_url!r}, "
            f"special_offers={self.special_offers!r}, labels={self.labels!r})"
        )
