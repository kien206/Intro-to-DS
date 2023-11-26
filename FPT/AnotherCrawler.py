import requests
import json
import csv

products = []

phone_page = "https://fptshop.com.vn/dien-thoai?trang={}"

product_detail_url = "https://fptshop.com.vn/api-data/API_GiaDung/api/Product/AppliancesAPI/GetProductDetail?name={}&url=https:%2F%2Ffptshop.com.vn%2Fdien-thoai%2F{}"
product_list_url = "https://fptshop.com.vn/apiFPTShop/Product/GetProductList?brandAscii=&url=https:%2F%2Ffptshop.com.vn%2Fdien-thoai%3Ftrang%3D{}%26pagetype%3D1"

product_id_file = "./data/fptproduct-id.txt"
product_data_file = "./data/fptproduct.txt"
product_file = "./data/fptproduct.csv"

# run product list API to get product ascii list for product detail API
def get_product_ascii():
    product_ascii_list = []
    i = 5
    response = requests.get(product_list_url.format(i))
    if (response.status_code == 200):
        product_ascii_list.append(response.text)
        print("Status code:", response.status_code,)
        
    return product_ascii_list

# process product ascii for product detail API
def process_product_ascii(product_ascii_json_list):
    product_ascii_list = []
    for product_ascii_json in product_ascii_json_list:
        e = json.loads(product_ascii_json)
        for products in e["datas"]["filterModel"]["listDefault"]["list"]:
            product_ascii_list.append(products["nameAscii"])
    return product_ascii_list

def crawl_product(product_list=[]):
    product_detail_list = []
    num = 1
    for product_acsii in product_list:
        response = requests.get(product_detail_url.format(product_acsii, product_acsii))
        if (response.status_code == 200):
            product_detail_list.append(response.text)
            print("Status code:", response.status_code, "Product number:", num)
            num += 1
    return product_detail_list

def process_product(product):
    e = json.loads(product)
    p = dict()
    name = e["datas"]["model"]["product"]["nameExt"]
    price = e["datas"]["model"]["orderModel"]['priceMarket']
    p["Tên"] = name
    for product_attribute in e["datas"]["model"]["product"]["productAttributes"]:
        attribute_name = product_attribute["attributeName"]
        attribute_value = product_attribute["specName"]
        p[attribute_name] = attribute_value
    p["Giá thị trường"] = price
    products.append(p)

    return p    

def save_to_csv(data):
    all_attributes = set()
    for entry in data:
        all_attributes.update(entry.keys())

    for entry in data:
        for attribute in all_attributes:
            if attribute not in entry:
                entry[attribute] = None

    csv_file = 'fptdata.csv'

    with open(csv_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_attributes)

        writer.writeheader()

        writer.writerows(data)

json_list = get_product_ascii()
product_ascii = process_product_ascii(json_list)
detail_list = crawl_product(product_ascii)
[process_product(product) for product in detail_list]
with open('fpt.json', 'w', encoding='utf-8') as j:
    for p in products:
        json.dump(p, j, ensure_ascii=False, indent=1)

save_to_csv(products)