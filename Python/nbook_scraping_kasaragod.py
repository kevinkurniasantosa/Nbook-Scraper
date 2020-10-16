import random
import string
import datetime
import requests
import re
from bs4 import BeautifulSoup
from pyexcel.cookbook import merge_all_to_a_book
import glob
import time
import csv
import unicodedata
import os
# Email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

print('import success')
start = time.time()

urls = [
    'https://nbook.in/city/kasaragod'
]
all_product = []

# Replace any error encoded character to csv become space
def clean_string(x):
    try:
        x = x.replace('\"','\'\'').replace('\r',' ').replace('\n',' ').replace(';', ' ')
        x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore')
        x = x.decode('ascii')
    except:
        x = '?'
    return x

def nbook_scraping():
    # Loop all URLs
    for url in urls:
        print('URL -> ' + url)
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text,'html.parser')
        
        # Get maximum pages
        pagination = soup.find('ul', class_='pagination').find_all('a')
        pages = pagination[17]
        x = re.match(".+data-ci-pagination-page=\"(.+)\" href.+", str(pages))
        pages = int(x.group(1)) 
        print('Max pages: ' + str(pages))

        # Loop all pages in each URL
        for page in range(pages):
            page_url = url + '/' + str(page+1)
            print('=========================')
            print('Scraping page ' + page_url)
            res = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            products = soup.find('div', class_='property-listing grid-view grid-view-3-col').find_all('div', class_='item-wrap')

            # Loop all products in each page
            for product in products:
                # Price-in-Letter
                try:
                    price_letter = clean_string(product.find('div', class_='price hide-on-list').h3.text.strip())
                    print('===================')
                except:
                    price_letter = '-'
                print(price_letter)

                # Title
                try:
                    title = clean_string(product.find('h2', class_='property-title').text)
                except:
                    title = '-'
                print(title)

                # Get product URL  
                try:
                    product_url = product.find('a', href=True)
                    print(product_url['href'])
                    url_url = product_url['href']
                    res = requests.get(product_url['href'], headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(res.text, 'html.parser')

                    # Status
                    try:
                        status = soup.find('address', class_='property-address').span.text.strip()
                    except:
                        status = '-'
                    print(status)
                    
                    # Numeric-Price
                    try:
                        numeric_price = clean_string(soup.find('span', class_='item-price').text.strip())
                    except:
                        numeric_price = '-'
                    print(numeric_price)

                    # Details and address product
                    try:
                        # details_content = soup.find('div', class_='detail-list detail-block slowload')
                        details_content = soup.find('div', class_='alert alert-info')
                        list_details = details_content.find('ul', class_='list-three-col').find_all('li')
                        # Old ID
                        try:
                            old_id = clean_string((list_details[0].text.strip()))
                            x = re.match('Property ID : (.+)', str(old_id))
                            old_id = x.group(1)
                        except: 
                            old_id = '-'

                        # Category Type
                        try:
                            category_type = clean_string((list_details[1].text.strip()))
                            x = re.match('Category : (.+)', str(category_type))
                            category_type = x.group(1)
                        except:
                            category_type = '-'

                        # Area_full/Property Size
                        try:
                            area_full = list_details[2].text.strip()
                            x = re.match('Property Size : (.+)', str(area_full))
                            area_full = x.group(1)
                        except:
                            area_full = '-'

                        if len(list_details) == 7:
                            # Bedrooms 
                            try:
                                bedrooms = list_details[4].text.strip()
                                x = re.match('Bedrooms : (.+)', str(bedrooms))
                                bedrooms = x.group(1)
                            except: 
                                bedrooms = '-'
                            
                            # Bathrooms
                            try:
                                bathrooms = list_details[5].text.strip()
                                x = re.match('Bathrooms : (.+)', str(bathrooms))
                                bathrooms = x.group(1)
                            except:
                                bathrooms = '-'
                        elif len(list_details) == 6: # IMPORTANT
                            # Bedrooms 
                            try:
                                bedrooms = list_details[3].text.strip()
                                x = re.match('Bedrooms : (.+)', str(bedrooms))
                                bedrooms = x.group(1)
                            except: 
                                bedrooms = '-'
                            
                            # Bathrooms
                            try:
                                bathrooms = list_details[4].text.strip()
                                x = re.match('Bathrooms : (.+)', str(bathrooms))
                                bathrooms = x.group(1)
                            except:
                                bathrooms = '-'
                        elif len(list_details) == 5:
                            # Bedrooms 
                            try:
                                bedrooms = list_details[2].text.strip()
                                x = re.match('Bedrooms : (.+)', str(bedrooms))
                                bedrooms = x.group(1)
                            except:
                                try:
                                    bedrooms = list_details[3].text.strip()
                                    x = re.match('Bedrooms : (.+)', str(bedrooms))
                                    bedrooms = x.group(1)
                                except:
                                    bedrooms = '-'
                            
                            # Bathrooms
                            try:
                                bathrooms = list_details[3].text.strip()
                                x = re.match('Bathrooms : (.+)', str(bathrooms))
                                bathrooms = x.group(1)
                            except:
                                try:
                                    bathrooms = list_details[4].text.strip()
                                    x = re.match('Bathrooms : (.+)', str(bathrooms))
                                    bathrooms = x.group(1)
                                except:
                                    bathrooms = '-'
                        elif len(list_details) == 4:
                            try:
                                bedrooms = list_details[2].text.strip()
                                x = re.match('Bedrooms : (.+)', str(bedrooms))
                                bedrooms = x.group(1)
                            except: 
                                bedrooms = '-'
                            # Bathrooms
                            try:
                                bathrooms = list_details[3].text.strip()
                                x = re.match('Bathrooms : (.+)', str(bathrooms))
                                bathrooms = x.group(1)
                            except:
                                bathrooms = '-'
                        else:
                            bedrooms = '-'
                            bathrooms = '-'
                    except:
                        old_id = '-'
                        category_type = '-'
                        area_full = '-'
                        bedrooms = '-'
                        bathrooms = '-'
                    print(old_id)
                    print(category_type)
                    print(area_full)
                    print(bedrooms)
                    print(bathrooms)

                    # Address
                    try:
                        address_content = soup.find('div', class_='detail-address detail-block slowload')
                        list_address = address_content.find('ul', class_='list-three-col').find_all('li')
                        # State
                        try:
                            state = list_address[1].text.strip()
                            x = re.match('State: (.+)', str(state))
                            state = x.group(1)
                        except:
                            state = '-'

                        # City
                        try:
                            city = list_address[2].text.strip()
                            x = re.match('City: (.+)', str(city))
                            city = x.group(1)
                        except:
                            city = '-'

                        # District
                        try:
                            district = list_address[4].text.strip()
                            x = re.match('District: (.+)', str(district))
                            district = x.group(1)
                        except:
                            district = '-'
                    except:
                        state = '-'
                        city = '-'
                        district = '-'
                    print(state)
                    print(city)
                    print(district)

                    # # Features
                    # try:
                    #     features_content = soup.find('div', class_='detail-features detail-block slowload')
                    #     list_features = features_content.find('ul', class_='list-three-col list-features').find_all('li')
                    #     features = []

                    #     for y in range(len(list_features)):
                    #         each_feature = list_features[y].text.strip()
                    #         # print(each_feature)
                    #         features.append(each_feature)
                    # except:
                    #     features = '-'
                    # print(features)

                    # Features
                    try:
                        features_content = soup.find('div', class_='detail-features detail-block slowload')
                        list_features = features_content.find('ul', class_='list-three-col list-features').find_all('li')

                        # Feature 1
                        try:
                            feature_1 = list_features[0].text.strip()
                        except:
                            feature_1 = '-'

                        # Feature 2 
                        try:
                            feature_2 = list_features[1].text.strip()
                        except:
                            feature_2 = '-'

                        # Feature 3 
                        try: 
                            feature_3 = list_features[2].text.strip()
                        except:
                            feature_3 = '-'
                    except:
                        feature_1 = '-'
                        feature_2 = '-'
                        feature_3 = '-'
                    print(feature_1)
                    print(feature_2)
                    print(feature_3)

                    # Contacts
                    try:
                        contacts = soup.find('div', class_='detail-contact detail-block slowload').find('div', class_='media-body').ul.find_all('li')
                        contact_name = clean_string(contacts[0].text.strip())
                        contact_phone = clean_string(contacts[1].span.text.strip())
                    except:
                        contact_name = '-'
                        contact_phone = '-'
                    print(contact_name)
                    print(contact_phone)
                    
                except Exception as err:
                    print('Error -> ' + str(err))

                data = {
                    'URL': url_url,
                    'Price-in-Letter': price_letter,
                    'Title': title,
                    'Status': status,
                    'Numeric-Price': numeric_price,
                    'Old-ID': old_id,
                    'Type': category_type,
                    'Area-full': area_full,
                    'Bedrooms': bedrooms,
                    'Bathrooms': bathrooms,
                    'Feature-1': feature_1,
                    'Feature-2': feature_2,
                    'Feature-3': feature_3,
                    'State': state,
                    'City': city,
                    'District': district,
                    'Contact-Name': contact_name,
                    'Contact-Phone': contact_phone
                }
                
                all_product.append(data)
                writer.writerow(data)

time.sleep(1)
print('\n==================')
print(all_product)

# Generate CSV
fieldnames=[
    'URL',
    'Price-in-Letter',
    'Title',
    'Status',
    'Numeric-Price',
    'Old-ID',
    'Type',
    'Area-full',
    'Bedrooms',
    'Bathrooms',
    'Feature-1',
    'Feature-2',
    'Feature-3',
    'State',
    'City',
    'District',
    'Contact-Name',
    'Contact-Phone'
]

filename_csv = 'Nbook Scraping Kasaragod.csv'
with open(filename_csv , 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    nbook_scraping()
    # for row in all_product:
    #     writer.writerow(row)
            
# Convert from CSV to Excel
filename_excel = 'Nbook Scraping Kasaragod.xlsx'
merge_all_to_a_book(glob.glob(filename_csv), filename_excel)

end = time.time()
run_time = end - start
run_time_hour = run_time/3600
print('Script runs for', round(run_time), 'seconds')
print('Script runs for', round(run_time_hour), 'hour(s)')


