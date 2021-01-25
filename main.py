''' Module 
args: https://www.autocentrum.pl
returns: array in pickle file of next teialed depth link, to final link of specified engine car version to be scraped
* def chape(lst) chekc if it is the end of depth tree
* def level1_car_fun() starts array and then goes to next ldepth levels in def get_all_levels() 

*last depth level level6_car.pickle -> def find_engine_versions()
*module returns arr of links in pickle all_car_engine_models.pickle
    '''
import requests
from scrapy import Selector
import pickle
import time


def add_front_link_part(car_list):
    for ind in range(0,len(car_list)):
        car_list[ind] = 'https://www.autocentrum.pl' + car_list[ind]
    return car_list

def level1_car_fun():
    html = requests.get('https://www.autocentrum.pl/dane-techniczne/').content
    sel = Selector(text = html)
    
    car_producers_links_list = sel.xpath('//div[@class="make-wrapper popular-make"]/a/@href').extract()
    car_not_popular_producers_links_list = sel.xpath('//div[@class="make-wrapper not-popular-make"]/a/@href').extract()
    car_producers_links_list += car_not_popular_producers_links_list
    car_producers_links_list = add_front_link_part(car_producers_links_list)
    level1_car_list = []
    for el in car_producers_links_list:
        html = requests.get(el).content
        sel = Selector(text = html)
        level1_car = sel.xpath('//div[@class="car-selector-box-row"]/a/@href').extract()
        level1_car = add_front_link_part(level1_car)
        level1_car_list += level1_car
    return level1_car_list


def shape(lst):
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length

def get_car_selector_box(level_car, my_xpath):
    
    new_level_car = []
    ind = 0
    while ind < len(level_car):
        try:
            print(ind , len(level_car), level_car[ind])
            html = requests.get(level_car[ind]).content
            sel = Selector(text = html)
            submodel = sel.xpath(my_xpath).extract()
            if len(submodel) != 0:
                submodel = add_front_link_part(submodel)
                new_level_car += submodel 
                print(submodel)
            else:
                new_level_car.append(level_car[ind])
            ind += 1

        except:
            print('error on index', ind)
            time.sleep(30)
            
    return new_level_car

def save_to_pickle(data_save, pickle_name):
    with open(pickle_name, 'wb') as my_pickle:
        pickle.dump(data_save, my_pickle)

def load_pickle(pickle_name):
    with open(pickle_name, 'rb') as my_pickle:
        return pickle.load(my_pickle)

def get_all_levels():
    level2_car = get_car_selector_box(level1_car_fun(), '//div[contains(@class, "car-selector-box-row")]/a/@href')
    print(shape(level2_car))
    save_to_pickle(level2_car,'level2_car.pickle')
    
    for i in range(3,7):
        level_car = get_car_selector_box(load_pickle('level{}_car.pickle'.format(i - 1)), '//div[contains(@class, "car-selector-box-row")]/a/@href')
        save_to_pickle(level_car,'level{}_car.pickle'.format(i))
        if shape(load_pickle('level{}_car.pickle'.format(i - 1))) == shape(load_pickle('level{}_car.pickle'.format(i))) :
            break
    print(shape(load_pickle('level{}_car.pickle'.format(i))))   

# get_all_levels()


def find_engine_versions(last_pickle):
    car_list = load_pickle(last_pickle)
    final_arr =[]
    ind = 0
    while ind < len(car_list):
        try:
            html = requests.get(car_list[ind]).content
            sel = Selector(text = html)
            engine = sel.xpath('//div[@class="engine-box visible"]/a/@href').extract()
            engine_full_link = add_front_link_part(engine)
            for el in engine_full_link:
                final_arr.append(el)
                print(el)
            ind += 1
            print(ind, car_list[ind])
        except:
            print('error on index', ind)
            time.sleep(10)
    save_to_pickle(final_arr, 'all_car_engine_models.pickle')
    
# find_engine_versions('level6_car.pickle')




