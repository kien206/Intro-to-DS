from selenium import webdriver
from bs4 import BeautifulSoup
import csv


driver = webdriver.Chrome() 

base_url = "https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang={}"

total_pages = 1 

all_phones_info = []
max_len=10

def get_data_from_url(url):
    driver = webdriver.Chrome()  
    driver.get(url)

    driver.implicitly_wait(5)

    page_source = driver.page_source

    driver.quit()
    soup = BeautifulSoup(page_source, 'html.parser')

    table = soup.find('table', class_='st-pd-table')

    attributes_list = dict()

    if table:
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:
                attribute = columns[0].text.strip()
                value = columns[1].text.strip()
                attributes_list[attribute]=value
    return attributes_list
count=0
for page in range(1, total_pages + 1):
    url = base_url.format(page)
    driver.get(url)
    driver.implicitly_wait(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    phone_urls = []
    product_info_divs = soup.find_all("div", class_="cdt-product__info")   
    for product_info in product_info_divs:
        phone_link = product_info.find("h3").find("a")
        if phone_link:
            phone_url = phone_link["href"]
            phone_urls.append(phone_url)
    for phone_url in phone_urls:
        full_phone_url = "https://fptshop.com.vn" + phone_url
        try:
            phone_info = get_data_from_url(full_phone_url)
            all_phones_info.append(phone_info)
        except Exception as e:
            print(f"Error processing {phone_url}: {str(e)}")
        count+=1
        if count==2:
            break
print(all_phones_info)
csv_filename = "phone_info.csv"
all_keys = set(key for phone_info in all_phones_info for key in phone_info)
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = sorted(all_keys)  
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(all_phones_info)
