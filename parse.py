from database import session_scope, create_car_table, create_car_image_table, create_all_tables
from bs4 import BeautifulSoup as bs
from selenium_scrapper import SeleniumScraper
import logging
from selenium_scrapper import webdriver
page_links = []
for num in range(1, 26):
    # page_link = f'https://www.alibaba.com/countrysearch/CN/car-auction_{num}.html'
    page_link = f'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.4bf33bdadf0Uyz&fsb=y&IndexArea=product_en&keywords=car+auction&tab=all&viewtype=G&&page={num}'
    page_links.append(page_link)
logging.warning(page_links)
# print(page_links)
scrapper = SeleniumScraper()
for url in page_links:
    # url = 'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.2f6c3bdaorFPJQ&tab=all&searchText=car+auction&viewtype=G'
    response = scrapper.get_response(url)
    soup = bs(response, 'html.parser')
    car_links = []
    marks = []  # Список марок
    tables = {}  # Список таблиц машин
    tables_img = {}  # Список таблиц фоток
    elements = soup.find_all(
        class_='fy23-search-card fy23-gallery-card m-gallery-product-item-v2 J-search-card-wrapper')
    for element in elements:
        link_element = element.find('a')
        if link_element:
            link = link_element['href']
            cleaned_link = link.replace('//', 'https://')
            car_links.append(cleaned_link)
    logging.warning(car_links)
    # print(car_links)
    for car_link in car_links:
        # car_url = 'https://www.alibaba.com/product-detail/Fairly-Used-Mercedes-Benzs-C63-AMG_1600905109956.html?spm=a2700.pc_countrysearch.main07.13.7947230fhXb8Gy'
        car_url = car_link
        response = scrapper.get_response(car_url)
        soup = bs(response, 'html.parser')
        # print(soup)

        attribute_lists = soup.find_all('div', class_='structure-table')
        if not attribute_lists:
            attribute_lists = soup.find_all('div', class_='attribute-list')

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
            if not attribute_items:
                attribute_items = attribute_list.find_all('div', class_='attribute-item')

            for attribute_item in attribute_items:
                left_element = attribute_item.find('div', class_='col-left')
                right_element = attribute_item.find('div', class_='col-right')
                if not left_element and right_element:
                    left_element = attribute_item.find('div', class_='left')
                    right_element = attribute_item.find('div', class_='right')
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
        try:
            my_price = soup.find('div', class_="price")
            price = my_price.text.strip().replace('CN¥', '').replace('/unit', '').replace('/set', '').replace('/piece',
                                                                                                              '').replace(
                '/sheet', '')
            if price:
                logging.warning(price)
            else:
                price = None
        except:
            price = None
        logging.warning(car_url)
        if marka:
            logging.warning(marka)
        else:
            marka = 'Other'
        if model:
            logging.warning(model)
        if year:
            logging.warning(year)
        if eco:
            logging.warning(eco)
        if kuzov:
            logging.warning(kuzov)
        if horse_power:
            logging.warning(horse_power)
        if privod:
            logging.warning(privod)
        if kpp:
            logging.warning(kpp)
        if kpp_type:
            logging.warning(kpp_type)
        if eng_v and not eng_info:
            logging.warning(eng_v)
        if eng_info and not eng_v:
            try:
                eng_v, hp, eng_type = eng_info.split(' ')
            except Exception:
                eng_v = None
                hp = None
                eng_type = None
            logging.warning(eng_info)
            logging.warning(eng_v)
            logging.warning(hp)
            logging.warning(eng_type)
            if not horse_power:
                horse_power = hp

        if mileage:
            logging.warning(mileage)
        with session_scope() as session:
            if marka and marka not in marks:
                marks.append(marka)
                table = create_car_table(marka)
                tables[marka] = table
                table_image = create_car_image_table(f'{marka}_image')
                tables_img[f'{marka}_image'] = table_image
                create_all_tables()
                rec = session.query(table).filter_by(xpath=car_url).first()
                if not rec:
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
                    try:
                        image_tags = soup.find("div", class_="detail-next-slick-track").find_all("div",
                                                                                                 class_="main-item")
                        if not image_tags:
                            image_tags = soup.find("div", class_="detail-next-slick-track").find_all("div",
                                                                                                     class_="detail-next-slick-slide detail-next-slick-active main-item false")
                    except Exception:
                        image_slider = soup.find('div', class_='image-list-slider')
                        image_tags = image_slider.find_all('img', class_='image-list-item')
                    for img_tag in image_tags:
                        try:
                            img = img_tag.find('img')
                            src = img['src']
                            if not src:
                                raise Exception
                        except Exception:
                            src = img_tag['src']
                            if not src:
                                scrapper.refresh_page()
                                continue
                        image_url = src.replace('140x140', '600x600').replace('100x100', '600x600')
                        logging.warning(image_url)
                        rec_image = tables_img[f'{marka}_image'](
                            car_id=rec.id,
                            image_url=image_url
                        )
                        session.add(rec_image)
                        session.commit()
                    logging.warning('car added succesfully')