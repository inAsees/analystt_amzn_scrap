from dataclasses import dataclass


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
