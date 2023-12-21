from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import time
import csv

def products_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup.prettify())

    # Targeting the <ul> element with id "product-grid"
    product_grid = soup.find('ul', id='product-grid')

    # Targeting the <li> elements within the <ul> element
    li_elements = product_grid.find_all('li')

    # Extracting the links from the <li> elements and joining with the base URL
    base_url = 'https://watchcollectors.co.uk'  # Replace with the actual base URL
    all_product = [urljoin(base_url, li.find('a')['href']) for li in li_elements if li.find('a')]

    return all_product

import warnings

# Suppress FutureWarnings for :contains
warnings.filterwarnings("ignore", category=FutureWarning, module="soupsieve")

imgUrls=[];productName=[];Price=[];modelNumber=[];modelYear=[];Gender=[];Diameter=[]
originalBox=[];originalPaper=[];productUrls=[]

def Product_details(links):
    c = 0
    for i in links:

        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            # image_urls = [img['data-src'] for img in soup.select('.media img[data-src]')]
            # imgUrls.append(image_urls)
            image_urls = [urljoin('https://', img['data-src']) for img in soup.select('.media img[data-src]')]
            imgUrls.append(image_urls)
        except:
            imgUrls.append('')

        productUrls.append(i)
        
        try:
            # product_title = soup.select_one('.product__title').get_text(strip=True)
            # productName.append(product_title)
            product_title = soup.find('td', string='Model').find_next('td').get_text(strip=True)
            productName.append(product_title)

        except:
            productName.append('')
            
        try:
            price = soup.find('span', {'class': 'price-item--regular'}).text.strip()
            print(price)
            Price.append(price)
        except:
            Price.append('')

        
        try:
            model_number = soup.find('td', string='Model Number').find_next('td').get_text(strip=True)
            modelNumber.append(model_number)
        except:
            modelNumber.append('')
    
        try:
            model_year = soup.find('td', string='Year').find_next('td').get_text(strip=True)
            modelYear.append(model_year )
        except:
            modelYear.append('')
    
        try:
            gender = soup.find('td', string='Gender').find_next('td').get_text(strip=True)
            Gender.append(gender)
        except:
            Gender.append('')

        try:
            diameter = soup.find('td', string='Diameter (mm)').find_next('td').get_text(strip=True)
            Diameter.append(diameter)
        except:
            Diameter.append('')

        try:
            original_box = soup.find('td', string='Original Box').find_next('td').get_text(strip=True)
            originalBox.append(original_box)
        except:
            originalBox.append('')
        
        try:
            original_papers = soup.find('td', string='Original Papers').find_next('td').get_text(strip=True)
            originalPaper.append(original_papers)
        except:
            originalPaper.append('')
        
        c = c + 1
        print(f"Product {c} completed.")

        time.sleep(5)  # Sleep for 5 seconds between requests
        
        if c==15:
            break
    data = {
    'Image Urls': [' '.join(img_urls) for img_urls in imgUrls],
    'Product Name': productName,
    'Price': Price,
    'Model Number': modelNumber,
    'Model Year': modelYear,
    'Gender': Gender,
    'Diameter': Diameter,
    'Original Box': originalBox,
    'Original Papers': originalPaper,
    'Product Url': productUrls}

    df = pd.DataFrame(data)
    # Writing to Excel file
    excel_file_path = 'output.xlsx'
    df.to_excel(excel_file_path, index=False)

    return True


#main Function
if __name__=="__main__": 
    # url = input("Enter Url: ")
    url = 'https://watchcollectors.co.uk/collections/all'
    all_links = products_links(url)
    print(all_links)
    details = Product_details(all_links)
    print(details)