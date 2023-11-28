from selenium import webdriver
from bs4 import BeautifulSoup
import csv
total_pages = 19
all_phones_info = []
base_url = "https://clickbuy.com.vn/dien-thoai?page={}"

# Initialize the WebDriver outside the loop
driver = webdriver.Chrome()

def get_data_from_url(url):
    driver.get(url)
    driver.implicitly_wait(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    table = soup.find('div', class_='product-specification__content')

    attributes_list = dict()

    if table:
        for row in table.find_all('tr'):
            # Use find instead of find_all to get individual elements
            attribute = row.find('th')
            value = row.find('td')

            # Check if both attribute and value are not None
            if attribute and value:
                attribute = attribute.text.strip()
                value = value.text.strip()
                attributes_list[attribute] = value
    price=soup.find("div",class_="product-price text-right")
    if price:
        value = price.find("p", class_="price").text
        numeric_value = ''.join(filter(str.isdigit, value))
        attributes_list["price"] = numeric_value
    name=soup.find("h1",class_="product-name")
    if name:
        attributes_list["name"]=name
    return attributes_list

for page in range(1, total_pages + 1):
    url = base_url.format(page)
    driver.get(url)
    driver.implicitly_wait(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    phone_urls = []
    product_info_divs = soup.find_all("div", class_="list-products__item")

    for product_info in product_info_divs:
        phone_link = product_info.find("a")
        if phone_link:
            phone_url = phone_link["href"]
            phone_name = phone_link["title"]
            phone_urls.append((phone_url, phone_name))

    for phone_url, phone_name in phone_urls:
        try:
            phone_info = get_data_from_url(phone_url)
            phone_info["name"] = phone_name
            all_phones_info.append(phone_info)
        except Exception as e:
            print(f"Error processing {phone_url}: {str(e)}")

# Move driver.quit() outside the loop
driver.quit()

print(all_phones_info)
csv_filename = "Clickbuy.csv"
all_keys = set(key for phone_info in all_phones_info for key in phone_info)
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    
    csv_writer = csv.DictWriter(csv_file, fieldnames=all_keys)
    csv_writer.writeheader()
    csv_writer.writerows(all_phones_info)