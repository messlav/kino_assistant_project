from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import time
import random
import csv

houses = []

with open('posutochno_org.csv', 'w') as csvfile:

    count = 1
    while count <= 100:
        
        html = urlopen("https://posutochno.org/moskva/?PAGEN_2=" + str(count))
        html_soup = BeautifulSoup(html, "html.parser")
        #print(html_soup)
        
        house_data = html_soup.findAll('div', class_='lcards cla')#.findAll('div', class_='lcards__item')
        house_data = house_data[1].findAll('div', class_='lcards__item')
        #print(house_data)
        
        if house_data != []:
            #print("gj")
            houses.extend(house_data)
            #value = random.random()
            #scaled_value = 1 + (value * (9 - 5))
            #time.sleep(scaled_value)
        #print(houses)
        else:
            break
        count += 1
        
    fieldnames = ['title', 'address', 'price', 'count_rooms', 'floor', 'type_obj', 'square', 'publication_date', 'link', 'images', 'metro', 'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    n = int(len(houses)) - 1
    #print(n)
    count = 0
    while count <= n:
        try:
            info = houses[int(count)]
            
            title = info.find('div', class_='lcards__name').get_text()
            #print(title)
            
            link = info.find('div', class_='lcards__photo')
            link = link.a
            link = link.get('href')
            link = 'https://posutochno.org' + link 
            #print(link)

            address = title.replace(" на ", "")
            address = address.replace("сутки", "", 1)
            address = address.replace("квартира", "", 1)
            address = address.replace("посуточно", "", 1)
            address = address.replace("комната", "", 1)
            address = address.replace("студия", "", 1)
            address = address.replace("Комната", "", 1)
            address = address.replace("Студия", "", 1)
            address = address.replace("Посуточно", "", 1)
            address = address.replace("Квартира", "", 1)
            address = address.replace("Сутки", "", 1)
            address = address.replace("1к ", "", 1)
            address = address.replace("2к ", "", 1)
            address = address.replace("3к ", "", 1)
            address = address.replace("4к ", "", 1)
            address = address.replace("5к ", "", 1)
            address = address.replace("6к ", "", 1)
            #print(title)
            #print(address)
            #break
            
            price = info.find('div', class_='lcards__label-price').get_text()
            price = price.replace("\n", "")
            price = price.replace(" ", "")
            price = price.replace("руб", "")
            price = price.replace(".", "")
            #print(price)
            
            type_obj = info.find('div', class_='lcards__label-type').get_text()
            type_obj = type_obj.replace("\n", "")
            type_obj = type_obj.replace("\t", "")
            if (type_obj[0] == '1' or type_obj[0] == '2' or type_obj[0] == '3' or type_obj[0] == '4' or type_obj[0] == '5'):
                type_obj = 'Квартира'
            #print(type_obj)
            
            if (type_obj == 'Студия' or type_obj == 'Комната'):
                count_rooms = 1
            else:
                count_rooms = info.find('div', class_='lcards__label-type').get_text()
                count_rooms = count_rooms.replace("\n", "")
                count_rooms = count_rooms.replace("\t", "")
                count_rooms = count_rooms.replace("комн", "")
            #print(count_rooms)
            
            
            #### ЗАХОДИМ ВНУТРЬ
            response = urlopen(link)
            html_soup = BeautifulSoup(response, 'html.parser')
            
            for_floor = html_soup.findAll('div', class_='options__wr-parameter clv')
            floor = 'no information'
            square = 'no information'
            for i in range (len(for_floor)) :
                if ('Этаж' in for_floor[i].get_text()):
                    floor = for_floor[i].get_text()
                    floor = floor.replace('\n', '')
                    floor = floor.replace('Этаж', '')
                if ('Площадь' in for_floor[i].get_text()):
                    square = for_floor[i].get_text()
                    square = square.replace('\n', '')
                    square = square.replace('Площадь', '')
            #print(floor)
            #print(square)
            #print(link, '\n')
            #print(for_floor, '\n')
            
            images = []
            for img in html_soup.findAll('li', class_='detailed-op__li'):
                img = img.find('a', onclick='return false;').get('href')
                img = 'https://posutochno.org' + img
                images.append(img)
                #print(img)
            #break
            
            
            phone = 'no information'
            #chrome_options = Options()
            #chrome_options.add_argument("--headless")
            #driver = webdriver.Chrome('/Users/slavapirogov/Downloads/chromedriver', options=chrome_options)
            #driver.get(link)
            #if 'btn-see-tel' in driver.page_source:
            #    button_element = driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[3]/div[1]/div[1]/div[1]/div/div/span[2]')
            #    button_element.click()
            #    if 'tel-number-user-text' in driver.page_source:
            #        phone = driver.find_element_by_class_name('tel-number-user-text')
            #        phone = phone.text
            #driver.close()
            #print(phone)
            
            
            publication_date = 'no information'
            metro = 'no information'
            
            csv_table = {'title':title, 'address':address, 'price':price, 'count_rooms':count_rooms, 'floor':floor, 'type_obj':type_obj, 'square':square, 'publication_date':publication_date, 'link':link, 'images':images, 'metro':metro, 'phone':phone}
            writer.writerow(csv_table)
            
            
        except AttributeError or IndexError:
            pass
        count += 1
        
