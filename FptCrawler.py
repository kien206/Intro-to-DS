import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import json

page = "https://fptshop.com.vn/dien-thoai?trang={}"

def get_all_page(url, num):
    lst = []
    for i in range(1, num+1):
        lst.append(url.format(i))
    return lst

def gather(page_lst):
    product_data = {} 
    data_list = []
    for page in page_lst:
        driver = webdriver.Chrome()
        driver.get(page)

        # Wait for the page to load (you may need to customize the waiting time)
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        prod_classes = soup.find_all("div", class_="cdt-product__info")
        count = 0
        for prod in prod_classes:
             # Store data for each product
            link = prod.find("h3").find("a")["href"]
            link = "https://fptshop.com.vn{}".format(link)
            print(link)

            # Parse the link page
            driver1 = webdriver.Chrome()
            driver1.get(link)
            driver1.implicitly_wait(5)
            link_soup = BeautifulSoup(driver1.page_source, 'html.parser')
            driver1.quit()

            # Find the table with the specific class
            table = link_soup.find("table", class_= "st-pd-table")
            name = link_soup.find("h1", class_= "st-name")
            product_data["Tên"] = name.text
            # Extract data from the table
            if table:
                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        attribute = columns[0].text.strip()
                        value = columns[1].text.strip()
                        product_data[attribute] = value
                data_list.append(product_data)
                product_data = {}
            count += 1
            if count==3:
                break

        # Sleep for a specified interval between requests
        time.sleep(1)  # Sleep for 2 seconds, adjust as needed

    return data_list

def save_to_json(data, filename="output"):
    json_file = '{}.json'.format(filename)
    with open(json_file, 'w', encoding="utf-8") as json_file:
        for phone in data:
            json.dump(phone, json_file, indent=1, ensure_ascii=False)

def save_to_csv(data):
    all_attributes = set()
    for entry in data:
        all_attributes.update(entry.keys())

    # Step 2: Ensure that each instance includes all attributes, even if some are missing
    for entry in data:
        for attribute in all_attributes:
            if attribute not in entry:
                entry[attribute] = None

    # Specify the CSV file path
    csv_file = 'output.csv'

    # Step 3: Write the data to a CSV file with all attributes as column headers
    with open(csv_file, 'w', newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_attributes)

        # Write the header
        writer.writeheader()

        # Write the data
        writer.writerows(data)

lst = get_all_page(page, 1)
res = gather(lst)
save_to_json(res)
save_to_csv(res)
print(res)
