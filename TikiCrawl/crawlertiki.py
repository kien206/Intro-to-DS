from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import json
import csv
smartphone_page_url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&version=home-persionalized&trackity_id=c5cb5655-3459-7d17-4ad8-46d964145677&category=1795&page={}&urlKey=dien-thoai-smartphone"
product_url = "https://tiki.vn/api/v2/products/{}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
all_attributes=set()
def crawl_product_id():
    product_list = []
    i = 1
    while i<16:
        print("Crawl page: ", i)
        response = requests.get(smartphone_page_url.format(i), headers=headers)
        
        if (response.status_code != 200):
            break

        products = json.loads(response.text)["data"]

        if (len(products) == 0):
            break

        for product in products:
            product_id = str(product["id"])
            print("Product ID: ", product_id)
            product_list.append(product_id)

        i += 1

    return product_list, i

def crawl_product(product_list=[]):
    product_detail_list = []

    for product_id in product_list:
        response = requests.get(product_url.format(product_id), headers=headers)

        try:
            # Check if the response contains valid JSON
            response_json = response.json()
        except json.decoder.JSONDecodeError:
            # If not, skip this product
            continue

        if response.status_code == 200:
            product_detail_list.append(response_json)

    return product_detail_list

def extract_product_info(product_detail,all_attributes):
    product_info = {}

    # Extract general information
    product_info["name"] = product_detail.get("name", "")
    product_info["price"] = product_detail.get("price", 0)   
    product_info["brand"] = product_detail.get("brand", {}).get("name", "")
    
    # Extract specifications
    specifications = product_detail.get("specifications", [])

    for spec_group in specifications:
        attributes = spec_group.get("attributes", [])

        for attribute in attributes:
            attr_code = attribute.get("code", "")
            attr_name = attribute.get("name", "")
            attr_value = attribute.get("value", "")

            attr_att = f"{attr_code.lower()}"

            # Add the attribute to the product_info dictionary
            product_info[attr_att] = attr_value
            all_attributes.add(attr_att)
    return product_info

product_list, page = crawl_product_id()
product_detail_list = crawl_product(product_list)

for product_detail in product_detail_list:
    extract_product_info(product_detail, all_attributes)
csv_file="tikidata.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as csv_file:
# Define CSV header based on all attributes
    fieldnames =["name","brand","price"]+ sorted(list(all_attributes))

    # Create a CSV writer
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header to the CSV file
    csv_writer.writeheader()

    # Write product information to the CSV file
    for product_detail in product_detail_list:
        product_info = extract_product_info(product_detail, all_attributes)
        csv_writer.writerow(product_info)

