import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
phone_api_url = "https://discovery.tekoapis.com/api/v1/product?sku={}&location=&terminalCode=phongvu"
page_url = "https://phongvu.vn/c/phone-dien-thoai?page={}"
total_pages = 4
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

all_attributes = set()
driver = webdriver.Chrome()

def crawl_product(phone_skus=[]):
    product_detail_list = []
    for phone_sku in phone_skus:
        api_url = phone_api_url.format(phone_sku)
        try:
            response = requests.get(api_url, headers=headers)
            response_json = response.json()
            if response.status_code == 200:
                product_detail_list.append(response_json)
        except json.decoder.JSONDecodeError:
            continue
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    return product_detail_list


def extract_product_info(product_detail, all_attributes):
    # Extract general information
    product_info = {}

    product_detail_ = product_detail.get("result", {}).get("product", {})
    product_info["name"] = product_detail_.get("productInfo", {}).get("name", "")
    # Check if "prices" list is not empty before accessing its first element
    prices = product_detail_.get("prices", [])
    if prices:
        product_info["price"] = prices[0].get("terminalPrice", "")
    else:
        product_info["price"] = ""
    product_info["brand"] = product_detail_.get("productInfo", {}).get("brand", {}).get("name", "")


    # Extract specifications
    attribute_groups_info = product_detail_.get("productDetail", {}).get("attributeGroups", [])

    for attribute in attribute_groups_info:
        attr_name = attribute.get("name", "")
        attr_value = attribute.get("value", "")

        attr_att = f"{attr_name.lower()}"

        # Add the attribute to the product_info dictionary
        product_info[attr_att] = attr_value
        all_attributes.add(attr_att)

    return product_info


        
phone_skus = []

for i in range(1, total_pages + 1):
    url = page_url.format(i)
    driver.get(url)
    driver.implicitly_wait(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    product_info_skus = soup.find_all("div", class_="css-13w7uog")
    for product_info in product_info_skus:
        info = product_info.find("div", class_="product-card css-1msrncq")
        sku = info["data-content-name"]
        phone_skus.append(sku)

driver.quit()

product_detail_list=crawl_product(phone_skus)

for product_detail in product_detail_list:
    extract_product_info(product_detail, all_attributes)

csv_filename = "PhongVu.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
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


