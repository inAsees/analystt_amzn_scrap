from dataclasses import dataclass
from typing import Dict

import requests as req
from bs4 import BeautifulSoup as bs


@dataclass
class ProductInfo:
    product_url: str
    product_name: str
    product_price: str
    ratings: int
    number_of_reviews: str
    description: str
    asin: str
    product_description: str
    manufacturer: str


class Scraper:
    def __init__(self, headers: Dict):
        self._headers = headers
        self._base_url = "https://www.amazon.in"
        self._page_nav_url = "https://www.amazon.in/s?k=bags&page=1&crid=2M096C61O4MLT&qid=1653504203&sprefix=" \
                             "ba%2Caps%2C283&ref=sr_pg_2"
        self._total_pages = self._get_total_pages(self._page_nav_url)
        self._total_nav_page_urls_list = [
            "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1653504203&sprefix=" \
            "ba%2Caps%2C283&ref=sr_pg_2".format(page_no) for page_no in range(self._total_pages + 1)]

    def _get_total_pages(self, page_nav_url: str) -> int:
        response = req.get(page_nav_url, headers=self._headers).text
        response_soup = bs(response, "html.parser")

        return int(response_soup.find("span", {"class": "s-pagination-item s-pagination-disabled"}).text)
