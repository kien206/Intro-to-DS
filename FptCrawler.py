import time
from bs4 import BeautifulSoup
from selenium import webdriver

page = "https://fptshop.com.vn/dien-thoai?trang={}"

def get_all_page(url, num):
    lst = []
    for i in range(1, num+1):
        lst.append(url.format(i))
    return lst

def gather(page_lst):
    product_data = {} 

    for page in page_lst:
        driver = webdriver.Chrome()
        driver.get(page)

        # Wait for the page to load (you may need to customize the waiting time)
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        prod_classes = soup.find_all("div", class_="cdt-product__info")

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
            table = link_soup.find('table', class_='st-pd-table')

            # Extract data from the table
            if table:
                for row in table.find_all('tr'):
                    columns = row.find_all('td')
                    if len(columns) == 2:
                        attribute = columns[0].text.strip()
                        value = columns[1].text.strip()
                        product_data[attribute] = value

        # Sleep for a specified interval between requests
        time.sleep(2)  # Sleep for 2 seconds, adjust as needed

    return product_data

lst = get_all_page(page, 1)
res = gather(lst)
print(res)
