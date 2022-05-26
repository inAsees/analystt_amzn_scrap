import re
from dataclasses import dataclass
from typing import Dict, Optional, List

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
    product_description: str
    asin: str
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
        self._product_info_list = []

    def scrap_all_pages(self) -> None:
        for url in self._total_nav_pages_url_list[:1]:
            response = req.get(url, headers=self._headers).text
            response_soup = bs(response, "html.parser")
            self._parse_product_overview(response_soup)

    def inject_info_in_product_overview(self) -> None:
        for ele in self._product_info_list:
            product_url = ele[0]
            response = req.get(product_url, headers=self._headers).text
            response_soup = bs(response, "html.parser")
            description = self._get_description(response_soup)
            asin = self._get_asin(response_soup)
            manufacturer = self._get_manufacturer(response_soup)

            print(asin)

    def _parse_product_overview(self, response_soup: bs) -> None:
        r_set = response_soup.findAll("div", {"data-component-type": "s-search-result"})
        for tag in r_set:
            product_url = self._get_product_url(tag)
            product_name = self._get_product_name(tag)
            product_price = self._get_product_price(tag)
            product_ratings = self._get_product_rating(tag)
            product_reviews = self._get_no_of_reviews(tag)
            self._product_info_list.append([product_url, product_name, product_price, product_ratings, product_reviews])

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
    def _get_product_rating(tag: Tag) -> Optional[str]:
        try:
            return tag.find("span", {"class": "a-icon-alt"}).text
        except AttributeError:
            return None

    @staticmethod
    def _get_no_of_reviews(tag: Tag) -> Optional[str]:
        try:
            return tag.find("span", {"class": "a-size-base s-light-weight-text"}).text
        except AttributeError:
            return None

    @staticmethod
    def _get_description(response_soup: bs) -> List[List[str]]:
        res = []
        r_set = response_soup.find("div", {"id": "feature-bullets"}).findAll("li")
        for txt in r_set:
            refined_text = txt.text.strip().replace("\n", "")
            res.append([refined_text])

        return res

    @staticmethod
    def _get_asin(response_soup: bs) -> Optional[str]:
        try:
            r_set = response_soup.find("div", {"id": "detailBulletsWrapper_feature_div"}).findAll("li")
        except AttributeError:
            return None
        for i in r_set:
            x = i.text.strip().encode("ascii", "ignore")
            y = x.decode().strip()
            z = re.sub("\s{1,}", " ", y).split(":")
            if "ASIN" in z[0]:
                return (z[1].strip())

    @staticmethod
    def _get_manufacturer(response_soup: bs) -> Optional[str]:
        try:
            r_set = response_soup.find("div", {"id": "detailBulletsWrapper_feature_div"}).findAll("li")
        except AttributeError:
            return None
        for i in r_set:
            x = i.text.strip().encode("ascii", "ignore")
            y = x.decode().strip()
            z = re.sub("\s{1,}", " ", y).split(":")
            if "Manufacturer" in z[0]:
                return (z[1].strip())

    def _get_total_pages(self, page_nav_url: str) -> int:
        response = req.get(page_nav_url, headers=self._headers).text
        response_soup = bs(response, "html.parser")

        return int(response_soup.find("span", {"class": "s-pagination-item s-pagination-disabled"}).text)
