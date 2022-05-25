from dataclasses import dataclass
from typing import Dict, List

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
        self._nav_page_url = "https://www.amazon.in/s?k=bags&page=1&crid=2M096C61O4MLT&qid=1653504203&sprefix=" \
                             "ba%2Caps%2C283&ref=sr_pg_2"
        self._total_nav_pages = self._get_total_pages(self._nav_page_url)
        self._total_nav_pages_url_list = ["https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=" \
                                          "1653504203&sprefix=ba%2Caps%2C283&ref=sr_pg_2".format(page_no) for page_no
                                          in range(1, self._total_nav_pages + 1)]
        self._product_info_list = []  # type: List[ProductInfo]

    def scrap_all_pages(self) -> None:
        page_no = 1
        for url in self._total_nav_pages_url_list:
            response = req.get(url, headers=self._headers).text
            response_soup = bs(response, "html.parser")
            self._scrap_url(response_soup, page_no)
            page_no += 1

    def _scrap_url(self, response_soup: bs, page_no: int) -> None:
        result_set = response_soup.findAll("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-"
                                                          "link-style a-text-normal"})
        for ele in result_set:
            url = self._base_url + ele.get("href")
            response = req.get(url, headers=self._headers).text
            response_soup = bs(response, "html.parser")
            product_info = self._parse_product_info(url, response_soup)
            self._product_info_list.append(product_info)

    def _parse_product_info(self, url: str, response_soup: bs) -> ProductInfo:
        product_url = url
        product_name = self._get_product_name(response_soup)
        product_price = self._get_product_price(response_soup)

        print(product_url, product_name, product_price)

    @staticmethod
    def _get_product_name(response_soup: bs) -> str:
        return response_soup.find("span", {"id": "productTitle"}).text.strip()

    @staticmethod
    def _get_product_price(response_soup: bs) -> str:
        return response_soup.find("span", {"class": "a-offscreen"}).text.strip()

    def _get_total_pages(self, page_nav_url: str) -> int:
        response = req.get(page_nav_url, headers=self._headers).text
        response_soup = bs(response, "html.parser")

        return int(response_soup.find("span", {"class": "s-pagination-item s-pagination-disabled"}).text)
