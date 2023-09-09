import re
import time

import aiohttp
from database import session_scope, create_car_table, create_car_image_table, create_all_tables
from bs4 import BeautifulSoup as bs
import requests
from selenium_scrapper import SeleniumScraper

page_links = []
for num in range(1,34):
    page_link = f'https://www.alibaba.com/countrysearch/CN/car-auction_{num}.html'
    page_links.append(page_link)
print(page_links)
for url in page_links:
# url = 'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.2f6c3bdaorFPJQ&tab=all&searchText=car+auction&viewtype=G'
    scrapper = SeleniumScraper()
    response = scrapper.get_response(url)
    # html_content = response.text
    # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div')
    # # scrapper.hover_over_element_by_class('sc-hd-lan')
    # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[3]/div/div/div[1]')
    # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[3]/div/div/div[2]/ul/li[2]/ul/li[20]')
    # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[5]')
    soup = bs(response, 'html.parser')
    # print(soup)
    # pag = soup.find('div', class_='class="l-sub-main-wrap util-clearfix')
    # print(pag)

    car_links = []
    marks = []  # Список марок
    tables = {}  # Список таблиц машин
    tables_img = {}  # Список таблиц фоток
    elements = soup.find_all(class_='search-card-e-slider__wrapper')
    for element in elements:
        link_element = element.find('a')
        if link_element:
            link = link_element['href']
            cleaned_link = link.replace('//', 'https://')
            car_links.append(cleaned_link)
    # scrapper.hover_over_element_by_class('sc-hd-lan')
    print(car_links)
    for car_link in car_links:
        # car_url = 'https://www.alibaba.com/product-detail/Fairly-Used-Mercedes-Benzs-C63-AMG_1600905109956.html?spm=a2700.pc_countrysearch.main07.13.7947230fhXb8Gy'
        car_url = car_link
        response = scrapper.get_response(car_url)
        # print(response)
        soup = bs(response, 'html.parser')
        # print(soup)

        # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div')
        # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[3]/div/div/div[1]')
        # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[3]/div/div/div[2]/ul/li[2]/ul/li[20]')
        # scrapper.click_element_by_xpath(xpath='//*[@id="J_SC_header"]/header/div[4]/div/div[4]/div[3]/div/div/div[2]/div[5]')

        # scrapper.click_element_by_class('css-1dimb5e-singleValue')
        # print(soup)
        # for_model = soup.find('div', class_="product-certifications")
        # print(for_model)
        # print(soup)
        # car_info = soup.find('div', class_='right')
        # print(car_info)
        attribute_lists = soup.find_all('div', class_='structure-table')
        marka = None
        model = None
        year = None
        eco = None
        kuzov = None
        horse_power = None
        privod = None
        kpp = None
        kpp_type = None
        eng_info = None
        mileage = None
        eng_v = None
        hp = None
        eng_type = None
        color = None
        lot_city = None
        price = None
        # my_price = None
        for attribute_list in attribute_lists:
            attribute_items = attribute_list.find_all('div', class_='structure-row')

            for attribute_item in attribute_items:
                left_element = attribute_item.find('div', class_='col-left')
                right_element = attribute_item.find('div', class_='col-right')

                model_obtained = False

                if left_element and left_element.text.strip() == "Brand Name":
                    marka = right_element.text.strip().split()[0].title()
                if left_element and left_element.text.strip() == "Make":  # ЕСЛИ НЕТ BRAND NAME
                    marka = right_element.text.strip().split()[0].title()
                if left_element and left_element.text.strip() == "Model Number" and not model_obtained:
                    model_el = right_element.text.strip()
                    first_space_index = model_el.find(" ")

                    if first_space_index != -1:
                        second_space_index = model_el.find(" ", first_space_index + 1)
                        if second_space_index != -1:
                            model = model_el[first_space_index + 1: second_space_index]
                        else:
                            model = right_element.text.strip()
                    else:
                        model = right_element.text.strip()
                    model_obtained = True

                if left_element and left_element.text.strip() == 'Product name' and not model_obtained:
                    model_el = right_element.text.strip()
                    first_space_index = model_el.find(" ")

                    if first_space_index != -1:
                        second_space_index = model_el.find(" ", first_space_index + 1)
                        if second_space_index != -1:
                            model = model_el[first_space_index + 1: second_space_index]
                        else:
                            model = right_element.text.strip()
                    else:
                        model = right_element.text.strip()
                    model_obtained = True

                if left_element and left_element.text.strip() == 'Model' and not model_obtained:
                    model_el = right_element.text.strip()
                    first_space_index = model_el.find(" ")

                    if first_space_index != -1:
                        second_space_index = model_el.find(" ", first_space_index + 1)
                        if second_space_index != -1:
                            model = model_el[first_space_index + 1: second_space_index]
                        else:
                            model = right_element.text.strip()
                    else:
                        model = right_element.text.strip()
                    model_obtained = True
                if left_element and left_element.text.strip() == "Year":
                    year = right_element.text.strip()
                if left_element and left_element.text.strip() == "Emission Standard":
                    eco = right_element.text.strip()
                if left_element and left_element.text.strip() == "Type":
                    kuzov = right_element.text.strip()
                if left_element and left_element.text.strip() == "Maximum horsepower (Ps)":
                    horse_power = right_element.text.strip()
                if left_element and left_element.text.strip() == "Horse Power":
                    horse_power = right_element.text.strip()
                if left_element and left_element.text.strip() == "Total engine power (kW)":
                    horse_power = right_element.text.strip()
                if left_element and left_element.text.strip() == "Motor rated power (KW)":
                    horse_power = right_element.text.strip()
                if left_element and left_element.text.strip() == "Motor total horsepower(Ps)":
                    horse_power = right_element.text.strip()
                if left_element and left_element.text.strip() == "Color":
                    color = right_element.text.strip()
                if left_element and left_element.text.strip() == "Appearance color":
                    color = right_element.text.strip()
                if left_element and left_element.text.strip() == 'Driving method':
                    privod = right_element.text.strip()
                if left_element and left_element.text.strip() == 'Place of Origin':
                    lot_city = right_element.text.strip()
                if left_element and left_element.text.strip() == 'Gear Box':
                    kpp = right_element.text.strip()
                if left_element and left_element.text.strip() == 'transmission':
                    kpp_type = right_element.text.strip()
                if left_element and left_element.text.strip() == "Engine":
                    eng_info = right_element.text.strip()
                if left_element and left_element.text.strip() == "Engines":
                    eng_info = right_element.text.strip()
                if left_element and left_element.text.strip() == "Engine Capacity":
                    eng_v = right_element.text.strip()
                if left_element and left_element.text.strip() == "Displacement":
                    eng_v = right_element.text.strip()
                if left_element and left_element.text.strip() == "Displacement (L)":
                    eng_v = right_element.text.strip()
                # if left_element and left_element.text.strip() == "Make":
                #     marka = right_element.text.strip()
                if left_element and left_element.text.strip() == "Mileage":
                    mileage = right_element.text.strip()
                if left_element and left_element.text.strip() == "Engine Type":
                    eng_type = right_element.text.strip()
        my_price = soup.find('div', class_="price")
        price = my_price.text.strip()
        if price:
            print('Цена:', my_price.text.strip())
        else:
            price = None

        print('xpath:', car_link)
        if marka:
            print("Марка машины:", marka)
        else:
            marka = 'Other'
        if model:
            print('Модель:', model)
        if year:
            print("Год выпуска:", year)
        if eco:
            print("Экологический класс:", eco)
        if kuzov:
            print("Кузов:", kuzov)
        if horse_power:
            print("Лощадиные силы:", horse_power)
        if privod:
            print("Привод:", privod)
        if kpp:
            print('Коробка передачь:', kpp)
        if kpp_type:
            print('Тип коробки:', kpp_type)
        if eng_v and not eng_info:
            print(eng_v)
        if eng_info and not eng_v:
            eng_v, hp, eng_type = eng_info.split(' ')
            print('Информация о двигателе:', eng_info)
            print(eng_v)
            print(hp)
            print(eng_type)
            if not horse_power:
                horse_power = hp

        if mileage:
            print('Пробег:', mileage)
        with session_scope() as session:
            if marka and marka not in marks:
                marks.append(marka)
                table = create_car_table(marka)
                tables[marka] = table
                table_image = create_car_image_table(f'{marka}_image')
                tables_img[f'{marka}_image'] = table_image
                create_all_tables()
            rec = tables[marka](
                xpath=car_url,
                model=model,
                year=year,
                color=color,
                kpp=kpp,
                lot_city=lot_city,
                mileage=mileage,
                kuzov=kuzov,
                eco=eco,
                price=price,
                eng_v=eng_v,
                kpp_type=kpp_type,
                horse_power=horse_power,
                engine_type=eng_type,
                privod=privod,
                status=1
            )
            session.add(rec)
            session.commit()
            image_slider = soup.find('div', class_='thumb-list')
            # print(image_slider)
            image_tags = image_slider.find_all('div', class_='detail-next-slick-slide detail-next-slick-active main-item false')
            # print(image_tags)
            # print(image_tags)
            for img_tag in image_tags:
                # print(img_tag)
                img = img_tag.find('img')
                src = img['src']
                # src = img_tag['src']
                image_url = src.replace('100x100', '600x600')
                print(image_url)
                rec_image = tables_img[f'{marka}_image'](
                    car_id=rec.id,
                    image_url=image_url
                )
                session.add(rec_image)
                session.commit()
# if my_price:
# print("Цена:", my_price.text.strip())
# pagination_div = soup.find('div', class_='l-sub-main-wrap util-clearfix')
# print(pagination_div)
# cars = soup.find('div', class_='m-gallery-product-item')
# if pagination_div:
#     pagination_links = pagination_div.find_all('a')
#
#     links = []
#     for link in pagination_links:
#         links.append(link['href'])
#
#     for link in links:
#         print(link)
# else:
#     print("Элемент 'ui2-pagination-pages' не найден.")
