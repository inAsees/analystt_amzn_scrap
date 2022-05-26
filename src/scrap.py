from dataclasses import dataclass
from typing import Dict, List

import requests as req
from bs4 import BeautifulSoup as bs, Tag


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
        self._nav_page_url = "https://www.amazon.in/s?k=bags&page=1&crid=2M096C61O4MLT&qid=1653504203&sprefix=" \
                             "ba%2Caps%2C283&ref=sr_pg_2"
        self._total_nav_pages = self._get_total_pages(self._nav_page_url)
        self._total_nav_pages_url_list = ["https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=" \
                                          "1653504203&sprefix=ba%2Caps%2C283&ref=sr_pg_{}".format(page_no, page_no) for
                                          page_no in range(1, self._total_nav_pages + 1)]
        self._product_info_list = []  # type: List[ProductInfo]

    def scrap_all_pages(self) -> None:
        for url in self._total_nav_pages_url_list:
            response = req.get(url, headers=self._headers).text
            response_soup = bs(response, "html.parser")
            self._parse_product_overview(response_soup)

    def _parse_product_overview(self, response_soup: bs) -> None:
        r_set = response_soup.findAll("div", {"data-component-type": "s-search-result"})
        for tag in r_set:
            product_name = self._get_product_name(tag)
            product_url = self._get_product_url(tag)
            product_price = self._get_product_price(tag)

            print(product_name, product_url, product_price)

    def _get_product_url(self, tag: Tag) -> str:
        url = tag.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-"
                                      "link-style a-text-normal"}).get("href")
        return self._base_url + url

    @staticmethod
    def _get_product_name(tag: Tag) -> str:
        return tag.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text

    @staticmethod
    def _get_product_price(tag: Tag) -> str:
        return tag.find("span", {"class": "a-offscreen"}).text

    @staticmethod
    def _get_product_rating(response_soup: bs) -> str:
        return response_soup.find("span", {"class": "a-icon-alt"}).text.strip()

    def _get_total_pages(self, page_nav_url: str) -> int:
        response = req.get(page_nav_url, headers=self._headers).text
        response_soup = bs(response, "html.parser")

        return int(response_soup.find("span", {"class": "s-pagination-item s-pagination-disabled"}).text)
