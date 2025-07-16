from bs4 import BeautifulSoup
from typing import Optional
import re

class Product:
    def __init__(self, raw_html: str):
        self.raw_html = raw_html
        soup = BeautifulSoup(raw_html, 'html.parser')
        li = soup.find('li')
        if not li:
            self.class_name = None
            self.value = None
            return
        self.class_name = ' '.join(li.get('class', []))
        self.value = {}
        # Attributes (except class)
        self.value['attributes'] = {k: v for k, v in li.attrs.items() if k != 'class'}
        # Description
        desc = None
        desc_tag = li.select_one('.description')
        if desc_tag:
            desc = desc_tag.get_text(strip=True)
        self.value['description'] = desc
        # Remove all children to get only direct text
        for child in li.find_all(recursive=False):
            child.extract()
        direct_text = li.get_text(strip=True)
        self.value['direct_text'] = direct_text
        # All visible text (no HTML tags)
        for script in li(['script', 'style']):
            script.decompose()
        self.value['all_visible_text'] = ' '.join(li.stripped_strings)

    def __repr__(self):
        return f"Product({self.class_name!r}: {self.value!r})"
