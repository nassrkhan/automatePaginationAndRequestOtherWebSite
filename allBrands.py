from bs4 import BeautifulSoup
import requests
import urllib.parse
from urllib.parse import urljoin
import time
import csv
import re
import pandas as pd

def brands_links():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}
    
    url = 'https://www.leguidedesmontres.com/en/products-new'

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with id "resultsBlk"
    results_div = soup.find('div', id='resultsBlk')

    # Extract links from all items
    relative_links = [item.a['href'] for item in results_div.find_all('div', class_='item')]

    # Extracting the links from the <li> elements and joining with the base URL
    base_url = 'https://www.leguidedesmontres.com'  # Replace with the actual base URL

    # Create complete URLs by concatenating with the base URL
    all_brands_links = [urllib.parse.urljoin(base_url, link) for link in relative_links]


    return all_brands_links

def products_links(brandsLink):
    all_products_links = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
        'AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/75.0.3770.80 Safari/537.36'}
    
    for i in brandsLink:

        response = requests.get(i, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with id "resultsBlk"
        results_div = soup.find('div', id='brands-results-main')

        # Extract links from all items
        relative_links = [item.a['href'] for item in results_div.find_all('div', class_='item')]

        # Extracting the links from the <li> elements and joining with the base URL
        base_url = "https://www.leguidedesmontres.com"  # Replace with the actual base URL

        # Create complete URLs by concatenating with the base URL
        all_products_links += [urllib.parse.urljoin(base_url, link) for link in relative_links]
        # all_products_links.extend([urllib.parse.urljoin(base_url, link) for link in relative_links])
    return all_products_links


def Product_details(links):
    imgUrls=[];productName=[];brandName=[];sku=[];Mouvement=[];Functions=[];Box=[];Bracelet=[]
    Remarks=[];Price=[];productUrls=[]
    c = 0
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
        'AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/75.0.3770.80 Safari/537.36'}
    for i in links:
        print(i)
        response = requests.get(i, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with id "product-details-info"
        product_details_info = soup.find('div', id='product-details-info')

        try:
            base_url = "https://www.leguidedesmontres.com"

            # Extract image URL
            relative_img_url = product_details_info.find('img', id='otherview-full-image')['src']

            # Create complete image URL by concatenating with the base URL
            img_url = urllib.parse.urljoin(base_url, relative_img_url)
            img_url = img_url.replace(" ", "")
            imgUrls.append(img_url)
            print(imgUrls)
        except:
            imgUrls.append('')

        productUrls.append(i)

        # Find the h2 element within the product-details-info div
        h2_element = soup.find('h2')

        try:
            # Extract product name
            brand_name = h2_element.contents[0].strip()
            brandName.append(brand_name)
            print(brandName)
        except:
            productName.append('')
        
        # Extract SKU number
        product_text = h2_element.span.get_text(strip=True)
        print(product_text)

        # Use regex to find all occurrences of text and numbers
        matches = re.findall(r'([a-zA-Z\s]*)([0-9.]+)', product_text)

        # Declare variables outside the loop
        # product_name = None
        # sku_number = None
        for match in matches:
            # Extract product name and SKU
            product_name = match[0].strip()
            sku_number = match[1].strip()


        try:
            sku.append(sku_number)
            print(sku)
        except:
            sku.append('')
        
        try:
            productName.append(product_name)
            print(productName)
        except:
            productName.append('')
        
        try:
            sku.append(number)
            print(sku)
        except:
            sku.append('')
        # Find the div with id "product-specs"
        product_specs = soup.find('div', id='product-specs')
        # print(product_specs)
        
        try:
            # Extract movement
            mouvement = product_specs.find('p', class_='detail-label', string='Mouvement').find_next('p', class_='detail-info').get_text(strip=True)
            Mouvement.append(mouvement)
            print(Mouvement)
        except:
            Mouvement.append('')

        try:
            # Extract function
            functions = product_specs.find('p', class_='detail-label', string='Functions').find_next('p', class_='detail-info').get_text(strip=True)
            Functions.append(functions)
            print(Functions)
        except:
            Functions.append('')

        try:
            # Extract box
            box = product_specs.find('p', class_='detail-label', string='Box').find_next('p', class_='detail-info').get_text(strip=True)
            Box.append(box)
            print(Box)
        except:
            Box.append('')

        try:
            # Extract bracelet
            bracelet = product_specs.find('p', class_='detail-label', string='Bracelet').find_next('p', class_='detail-info').get_text(strip=True)
            Bracelet.append(bracelet)
            print(Bracelet)
        except:
            Bracelet.append('')
        
        try:
            # Extract remarks
            remarks = product_specs.find('p', class_='detail-label', string='Remarks').find_next('p', class_='detail-info').get_text(strip=True)
            Remarks.append(remarks)
            print(Remarks)
        except:
            Remarks.append('')
        
        # Extract Price
        price_detail = product_details_info.find('div', class_='price-detail')

        try:
            # Extract price
            price = price_detail.find('p', class_='detail-info').get_text(strip=True)
            Price.append(price)
            print(Price)
        except:
            Price.append('')

        c = c + 1
        print(f"Product {c} completed.")

        time.sleep(5)  # Sleep for 5 seconds between requests
        
        if c==2:
            break
    # Remove None and empty strings
    sku = [item for item in sku if item is not None and str(item).strip() != '']
    # Assuming imgUrls, sku, and other lists have different lengths
    max_length = max(len(imgUrls), len(sku), len(brandName), len(productName), len(Mouvement), len(Functions), len(Box), len(Bracelet), len(Remarks), len(Price), len(productUrls))

    # Fill shorter lists with NaN to match the max length
    imgUrls += [None] * (max_length - len(imgUrls))
    sku += [None] * (max_length - len(sku))
    brandName += [None] * (max_length - len(brandName))
    productName += [None] * (max_length - len(productName))
    Mouvement += [None] * (max_length - len(Mouvement))
    Functions += [None] * (max_length - len(Functions))
    Box += [None] * (max_length - len(Box))
    Bracelet += [None] * (max_length - len(Bracelet))
    Remarks += [None] * (max_length - len(Remarks))
    Price += [None] * (max_length - len(Price))
    productUrls += [None] * (max_length - len(productUrls))
    image_urls_list = [' '.join(img_urls) if img_urls else None for img_urls in imgUrls]
    data = {
        'Image Urls': image_urls_list,
        'SKU': sku,
        'Brand Name': brandName,
        'Product Name': productName,
        'Mouvement': Mouvement,
        'Functions': Functions,
        'Box': Box,
        'Bracelet': Bracelet,
        'Remarks': Remarks,
        'Price': Price,
        'Product Url': productUrls
    }

    df = pd.DataFrame(data)

    # Writing to Excel file
    excel_file_path = 'output1.xlsx'
    df.to_excel(excel_file_path, index=False)

    return True    

#main Function
if __name__=="__main__":
    brandsLink = brands_links() 
    productLink = products_links(brandsLink)
    len(productLink)
    pro = Product_details(productLink)
    