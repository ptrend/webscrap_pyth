'''
args: last depth pickle
returns: array in pickle final_data26486.pickle, there are 26486 car engine unique versions

*def xpath_ind() returns name of specification like: car length, width, engine cylinder numbers...
*def xpath_value() returns value of def xpath_ind()
*normalize_dict(dictionary) gives readable values

*def run_car_details():
    runs all links from last depth level of car details level6_car.pickle
    
    while loop used to control flow of elements of array(level6_car.pickle), 
    if error sleeps 30 second and goes until gets data or error_numbers == 3,
    errors on no internet event
    
    saves data in pickles from 0 to counter % 5000 == 0,
    gives increasing array in pickles, end pickle saves on end of while loop (level6_car.pickle)
    
    on my personal computer i5-4288U 2.6GHz it took about 17 hours
 '''
import requests
from scrapy import Selector
import main
import time
import unicodedata

def xpath_ind(group_i, row_i, data_content):
    if data_content == 'car_info':
        left_side_xpath = '//div[@class="dt-main-header"]/following-sibling::div[1]/div[@class="col-md-6"][1]/div[@class="group"][{}]/div[@class="dt-row"][{}]/div[@class="dt-row__text"]/@data-label'.format(group_i, row_i)
    elif data_content == 'car_engine':
        left_side_xpath = '//div[@class="margin25"]/div[@class="row"]/div[@class="col-md-6"]/div[@class="group"][{}]/div[@class="dt-row"][{}]/div[@class="dt-row__text"]/@data-label'.format(group_i, row_i)
    return left_side_xpath

def xpath_value(group_i, row_i, data_content):
    if data_content == 'car_info':
        left_side_xpath = '//div[@class="dt-main-header"]/following-sibling::div[1]/div[@class="col-md-6"][1]/div[@class="group"][{}]/div[@class="dt-row"][{}]/div[@class="dt-row__text"]/../div[2]/span/text()'.format(group_i, row_i)
    elif data_content == 'car_engine':
        left_side_xpath = '//div[@class="margin25"]/div[@class="row"]/div[@class="col-md-6"]/div[@class="group"][{}]/div[@class="dt-row"][{}]/div[@class="dt-row__text"]/following-sibling::div/span/text()'.format(group_i, row_i)
    return left_side_xpath

def normalize_dict(dictionary):
    for key in dictionary:
        dictionary[key] = unicodedata.normalize("NFKD", dictionary[key])

counter = 0
def run_car_details():
    main_arr = []
    database = main.load_pickle('all_car_engine_models.pickle')

    link_ind = 0
    error_numbers = 0
    
    while link_ind < len(database):
        try:
            link = database[link_ind]
            html = requests.get(link).content
            sel = Selector(text = html)
            
            door_no = 'none'
            seats_no = 'none'
            diameter = 'none'
            radius = 'none'
            car_length = 'none'
            car_width = 'none'
            car_width_mirrors = 'none'
            car_height = 'none'
            car_height_plus_railings = 'none'
            car_height_plus_back_doors = 'none'
            car_axes_length = 'none'
            car_wheels_front_width = 'none'
            car_wheels_back_width = 'none'
            car_clearance = 'none'
            car_trunk_max = 'none'
            car_trunk_min = 'none'
            row_1_car_info = ''
            row_2_car_info = ''
            row_3_car_info = ''
            #1
            all_existing_car_data = sel.xpath('//div[@class="dt-main-header"]/following-sibling::div[1]/div[@class="col-md-6"][1]/h3/text()').extract()
            for ind, existing_car_data in enumerate(all_existing_car_data):
                try:
                    if existing_car_data == 'Podstawowe parametry ':
                        row_1_car_info = ind + 1
                    if existing_car_data == 'Wymiary zewnętrzne ':
                        row_2_car_info = ind + 1
                    if existing_car_data == 'Wymiary bagażnika ':
                        row_3_car_info = ind + 1
                except:
                    x = 'error ind #1'
            #2        
            if row_1_car_info:
                for row_i in range(1,5):
                    try:
                        primary_data_ind = sel.xpath(xpath_ind(row_1_car_info, row_i,'car_info')).extract()[0]
                        primary_data_value = sel.xpath(xpath_value(row_1_car_info, row_i,'car_info')).extract()[0]
                        if primary_data_ind == 'Liczba drzwi':
                            door_no = primary_data_value
                        elif primary_data_ind == 'Liczba miejsc':
                            seats_no = primary_data_value
                        elif primary_data_ind == 'Średnica zawracania':
                            diameter = primary_data_value
                        elif primary_data_ind == 'Promień skrętu':
                            radius = primary_data_value
                    except:
                        x = 'error ind #2'
            #3            
            if row_2_car_info:
                for row_i in range(1,11):
                    try:
                        primary_data_ind = sel.xpath(xpath_ind(row_2_car_info, row_i,'car_info')).extract()[0]
                        primary_data_value = sel.xpath(xpath_value(row_2_car_info, row_i,'car_info')).extract()[0]
                        if primary_data_ind == 'Długość':
                            car_length = primary_data_value
                        elif primary_data_ind == 'Szerokość':
                            car_width = primary_data_value
                        elif primary_data_ind == 'Szerokość z lusterkami bocznymi':
                            car_width_mirrors = primary_data_value
                        elif primary_data_ind == 'Wysokość':
                            car_height = primary_data_value
                        elif primary_data_ind == 'Wysokość z relingami dachowymi':
                            car_height_plus_railings = primary_data_value
                        elif primary_data_ind == 'Wysokość przy otwartej klapie bagażnika':
                            car_height_plus_back_doors = primary_data_value
                        elif primary_data_ind == 'Rozstaw osi':
                            car_axes_length = primary_data_value
                        elif primary_data_ind == 'Rozstaw kół - przód':
                            car_wheels_front_width = primary_data_value
                        elif primary_data_ind == 'Rozstaw kół - tył':
                            car_wheels_back_width = primary_data_value
                        elif primary_data_ind == 'Prześwit':
                            car_clearance = primary_data_value
                    except:
                        x = 'error ind #3'
            #4            
            if row_3_car_info:
                for row_i in range(1,3):
                    try:
                        primary_data_ind = sel.xpath(xpath_ind(row_3_car_info, row_i,'car_info')).extract()[0]
                        primary_data_value = sel.xpath(xpath_value(row_3_car_info, row_i,'car_info')).extract()[0]
                        if primary_data_ind == 'Maksymalna pojemność bagażnika (siedzenia złożone)':
                            car_trunk_max = primary_data_value
                        elif primary_data_ind == 'Minimalna pojemność bagażnika (siedzenia rozłożone)':
                            car_trunk_min = primary_data_value
                    except:
                        x = 'error ind #4'
            #5
            all_existing_engine_data = sel.xpath('//div[@class="margin25"]/div[@class="row"]/div[@class="col-md-6"]/h3/text()').extract()
            for ind, existing_engine_data in enumerate(all_existing_engine_data):
                try:
                    if existing_engine_data == 'Podstawowe parametry ':
                        row_1_engine_info = ind + 1
                except:
                    x = 'error ind #5'
                    
            car_engine_produced = 'none'
            car_engine_v = 'none'
            car_engine_type = 'none'
            car_engine_power = 'none'
            car_engine_torque = 'none'
            car_engine_line = 'none'
            car_engine_cylinders = 'none'
            car_engine_cylinders_line = 'none'
            car_engine_valve_numbers = 'none'
            car_engine_compression_ratio = 'none'
            car_engine_cyl_info = 'none'
            car_engine_ignition = 'none'
            car_engine_injection_type = 'none'
            #6
            for row_i in range(1,15):
                try:
                    primary_data_ind = sel.xpath(xpath_ind(row_1_engine_info, row_i,'car_engine')).extract()[0]
                    primary_data_value = sel.xpath(xpath_value(row_1_engine_info, row_i,'car_engine')).extract()[0]
                    if primary_data_ind == 'Produkowany':
                        car_engine_produced = primary_data_value
                    elif primary_data_ind == 'Pojemność skokowa':
                        car_engine_v = primary_data_value
                    elif primary_data_ind == 'Typ silnika':
                        car_engine_type = primary_data_value
                    elif primary_data_ind == 'Moc silnika':
                        car_engine_power = primary_data_value
                    elif primary_data_ind == 'Maksymalny moment obrotowy':
                        car_engine_torque = primary_data_value
                    elif primary_data_ind == 'Montaż silnika':
                        car_engine_line = primary_data_value
                    elif primary_data_ind == 'Liczba cylindrów':
                        car_engine_cylinders = primary_data_value
                    elif primary_data_ind == 'Układ cylindrów':
                        car_engine_cylinders_line = primary_data_value
                    elif primary_data_ind == 'Liczba zaworów':
                        car_engine_valve_numbers = primary_data_value
                    elif primary_data_ind == 'Stopień sprężania':
                        car_engine_compression_ratio = primary_data_value
                    elif primary_data_ind == 'Średnica cylindra × skok tłoka':
                        car_engine_cyl_info = primary_data_value
                    elif primary_data_ind == 'Zapłon':
                        car_engine_ignition = primary_data_value
                    elif primary_data_ind == 'Typ wtrysku':
                        car_engine_injection_type = primary_data_value
                except:
                    x = 'error ind #6'

            #7
            try:
                config_box_xpath = '//div[@class="engine-configuration margin25"]/div[@class="row"]/div[@class="col-md-6"][1]/div[@class="config-box"]'
                gear_list = sel.xpath(config_box_xpath).extract()
                gear_list_count = len(gear_list)
                
                gear_arr = []
                for ind in range(1, gear_list_count + 1):
                    try:
                        groups_xpath = config_box_xpath + '[{}]/div[@class="group"]'.format(ind)
                        groups_count = sel.xpath(groups_xpath).extract()
                        groups_count = len(groups_count)
                        gear_type = 'none'
                        gear_no = 'none'
                        drive_type = 'none'
                        V_max = 'none'
                        acceleration = 'none'
                        fuel_ave = 'none'
                        fuel_road = 'none'
                        fuel_city = 'none'
                        V_fuel = 'none'
                        range_ave = 'none'
                        range_road = 'none'
                        range_city = 'none'
                        co2 = 'none'
                        euro_type = 'none'
                        weight_min = 'none'
                        weight_max = 'none'
                        
                        for ind_group in range(1, groups_count + 1):
                            dt_row_xpath = groups_xpath + '[{}]/div[@class="dt-row"]'.format(ind_group)
                            dt_row_count = sel.xpath(dt_row_xpath).extract()
                            dt_row_count = len(dt_row_count)
                            
                            for ind_row in range(1, dt_row_count + 1):
                                row_text = dt_row_xpath + '[{}]/div[@class="dt-row__text"]/@data-label'.format(ind_row)
                                row_text = sel.xpath(row_text).extract()
                                rodzaj_skrzyni_xpath = dt_row_xpath + '[{}]/div[@class="dt-row__value right-value"]/span/text()'.format(ind_row)

                                try:
                                    if row_text[0] == 'Rodzaj skrzyni':
                                        gear_type = sel.xpath(rodzaj_skrzyni_xpath).extract()[0]
                                    elif row_text[0] == 'Liczba biegów' or row_text[0] == 'Liczba stopni':
                                        gear_no = sel.xpath(rodzaj_skrzyni_xpath).extract()[0]
                                    elif row_text[0] == 'Rodzaj napędu':
                                        drive_type = sel.xpath(rodzaj_skrzyni_xpath).extract()[0]  
                                    elif row_text[0] == 'Prędkość maksymalna':
                                        V_max = sel.xpath(rodzaj_skrzyni_xpath).extract()[0]  
                                    elif row_text[0] == 'Przyspieszenie (od 0 do 100km/h)':
                                        acceleration = sel.xpath(rodzaj_skrzyni_xpath).extract()[0]      
                                    elif row_text[0] == 'Średnie spalanie (cykl mieszany)':
                                        fuel_ave = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Spalanie na trasie (na autostradzie)':
                                        fuel_road = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Spalanie w mieście':
                                        fuel_city = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Pojemność zbiornika paliwa':
                                        V_fuel = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Zasięg (cykl mieszany)':
                                        range_ave = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Zasięg (autostrada)':
                                        range_road = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Zasięg (miasto)':
                                        range_city = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Emisja CO₂':
                                        co2 = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Norma emisji spalin':
                                        euro_type = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Minimalna masa własna pojazdu (bez obciążenia)':
                                        weight_min = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 
                                    elif row_text[0] == 'Maksymalna masa całkowita pojazdu (w pełni obciążonego)':
                                        weight_max = sel.xpath(rodzaj_skrzyni_xpath).extract()[0] 

                                except:
                                    print(x)
                        gear_temp_dict = {}
                        gear_temp_dict = {
                            'gear_type': gear_type,
                            'gear_no': gear_no,
                            'drive_type': drive_type,
                            'V_max': V_max,
                            'acceleration': acceleration,
                            'fuel_ave': fuel_ave,
                            'fuel_road':fuel_road,
                            'fuel_city': fuel_city,
                            'V_fuel': V_fuel,
                            'range_ave': range_ave,
                            'range_road': range_road,
                            'range_city': range_city,
                            'co2': co2,
                            'euro_type': euro_type,
                            'weight_min': weight_min,
                            'weight_max': weight_max
                            }
                        normalize_dict(gear_temp_dict)
                        gear_arr.append(gear_temp_dict)

                    except:
                        print('error with one of gear boxes')
            except:
                x = 'error ind #7 gear list'
                print(x)
                


            car_id = ' '
            car_id = car_id.join(sel.xpath('//ol/li/a/span/text()').extract()[2:])
            dict_temp = {}
            dict_temp = {
                'car_id': car_id,
                'link': link,
                'car_primary' : {
                    'door_no': door_no,
                    'seats_no': seats_no,
                    'diameter': diameter,
                    'radius': radius,
                    'car_length': car_length,
                    'car_width': car_width,
                    'car_width_mirrors': car_width_mirrors,
                    'car_height': car_height,
                    'car_height_plus_railings': car_height_plus_railings,
                    'car_height_plus_back_doors': car_height_plus_back_doors,
                    'car_axes_length': car_axes_length,
                    'car_wheels_front_width': car_wheels_front_width,
                    'car_wheels_back_width': car_wheels_back_width,
                    'car_clearance': car_clearance, 
                    'car_trunk_max': car_trunk_max,
                    'car_trunk_min': car_trunk_min,
                    'car_engine_produced': car_engine_produced,
                    'car_engine_v': car_engine_v,
                    'car_engine_type': car_engine_type,
                    'car_engine_power': car_engine_power,
                    'car_engine_torque': car_engine_torque,
                    'car_engine_line': car_engine_line,
                    'car_engine_cylinders': car_engine_cylinders,
                    'car_engine_cylinders_line': car_engine_cylinders_line,
                    'car_engine_valve_numbers': car_engine_valve_numbers,
                    'car_engine_compression_ratio': car_engine_compression_ratio,
                    'car_engine_cyl_info': car_engine_cyl_info,
                    'car_engine_ignition': car_engine_ignition,
                    'car_engine_injection_type': car_engine_injection_type
                    },
                'transmission': gear_arr
                }
            normalize_dict(dict_temp['car_primary'])
            
            main_arr.append(dict_temp)
            
            link_ind += 1
            error_numbers = 0
            
            global counter
            counter += 1
            print(counter, link)
            if counter % 5000 == 0:
                main.save_to_pickle(main_arr, 'final_data{}.pickle'.format(counter))
        except:
            print('error_catched', link, error_numbers)
            time.sleep(30)
            error_numbers += 1
            if error_numbers == 3:
                link_ind += 1
                
    main.save_to_pickle(main_arr, 'final_data{}.pickle'.format(counter))            
    return main_arr                

run_car_details()

