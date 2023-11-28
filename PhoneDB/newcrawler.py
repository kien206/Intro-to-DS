from selenium import webdriver
from bs4 import BeautifulSoup
import csv

total_pages =50
all_phones_info = []
driver = webdriver.Chrome()

def crawl_data_from_url(url):
    driver.get(url)
    driver.implicitly_wait(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    attribute_rows = soup.find_all("tr")
    attributes_values = {}

    # Loop through each row and extract attribute-value pairs
    for row in attribute_rows:
        # Extract attribute and value
        attribute = row.find('strong')

        if attribute:
            attribute_text = attribute.text.strip()

            # Find the next sibling <td> tag as the value
            value_tag = attribute.find_next('td')
            if value_tag:
                value_text = value_tag.text.strip()
                attributes_values[attribute_text] = value_text
    # Find the <td> tag containing <a id="datasheet_item_id499"></a>
    target_a = soup.find('a', id='datasheet_item_id499')

    # Extract the text content from the parent <td> tag
    if target_a:
        target_td = target_a.find_parent('td')
        target_text = target_td.get_text(strip=True)
        attributes_values["currency"]=target_text
    return attributes_values
phone_urls = []
base_url = "https://phonedb.net/index.php?m=device&s=list&filter={}"
for page in range(1, total_pages + 1):
    url = base_url.format(page)
    driver.get(url)
    driver.implicitly_wait(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    product_info_divs = soup.find_all("div", class_="content_block")

    for product_info in product_info_divs:
        pro_info = product_info.find("div", class_="content_block_title")
        if pro_info:
            phone_link = pro_info.find("a")
            if phone_link:
                phone_url = "https://phonedb.net/"+phone_link["href"]
                phone_urls.append(phone_url)
for phone_url in phone_urls:
    phone_info=crawl_data_from_url(phone_url)
    all_phones_info.append(phone_info)


driver.quit()
csv_filename = "PhoneDatabase.csv"
all_keys = set(key for phone_info in all_phones_info for key in phone_info)
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=all_keys)
    csv_writer.writeheader()
    csv_writer.writerows(all_phones_info)