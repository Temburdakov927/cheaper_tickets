from datetime import datetime
from enum import Enum
import time
import requests
from parsing_city_Russia import find_iso_and_city


tickets = None
#Текущее время и дата, для отображения времени создания записи в базе данных
date_create = str(datetime.today().date())
time_create = time.strftime("%H:%M", time.localtime())

#Список из iso разных городов, в данной версии программы не используется
cities = ['HAK', 'TUU', 'NCE', 'KLF', 'AKX', 'VVO', 'GRV', 'MRS', 'CAN', 'YYT', 'ENE', 'OSA', 'CPT', 'NAL', 'JRO', 'CJU', 'MED', 'UTH', 'BAH', 'PKV', 'IGR', 'EAP', 'LWN', 'RIX', 'TGD', 'JAN', 'YYC', 'SOF', 'SUB', 'CAI', 'UUD', 'LED', 'BTU', 'SEL', 'DTM', 'ABA', 'FRA', 'MFM', 'IKT', 'CUZ', 'FLL', 'TLL', 'COV', 'TNR', 'UIO', 'TPS', 'GRO', 'BAK', 'PQC', 'VAN', 'PUY', 'DUR', 'FLN', 'BUH', 'UGC', 'GOJ', 'MRU', 'KEJ', 'FOR', 'TRV', 'IZM', 'REN', 'VAR', 'PER', 'MTS', 'FRU', 'FEG', 'SPU', 'EDI', 'TOS', 'YTO', 'SAO', 'BGO', 'PHL', 'BER', 'PAR', 'CUN', 'SAI', 'LGK', 'RBA', 'SKD', 'VGO', 'TIA', 'VIE', 'SCL', 'ZTH', 'OAX', 'TYO', 'MAH', 'HRB', 'BOJ', 'STR', 'LIM', 'FTE', 'JUJ', 'NLP', 'AER', 'DEN', 'JOG', 'FUE', 'GYE', 'VRA', 'PXM', 'CHI', 'TIJ', 'SCY', 'ATL', 'EFL', 'NQZ', 'BUD', 'KUF', 'SJJ', 'TUN', 'HAN', 'FUK', 'SZX', 'VFA', 'DUS', 'SYX', 'SRE', 'KGD', 'CTA', 'ZRH', 'CDT', 'KVA', 'KRK', 'BWI', 'ASE', 'YYJ', 'MGA', 'MSQ', 'LRH', 'PUJ', 'STO', 'BRU', 'IST', 'FMM', 'JTR', 'TPE', 'SVQ', 'MMA', 'UFA', 'LIL', 'LAS', 'BUS', 'ISG', 'TLS', 'SCO', 'HOR', 'DLM', 'HER', 'GPS', 'JKH', 'PNH', 'YOW', 'DYU', 'MOQ', 'NGS', 'MBJ', 'DNZ', 'KTW', 'GDL', 'CNX', 'SSA', 'CGN', 'JKT', 'STW', 'TIV', 'KTM', 'SPC', 'YXE', 'MRV', 'IAO', 'EVN', 'KHV', 'AHO', 'GME', 'BKI', 'VXE', 'SJU', 'PVD', 'STL', 'HRE', 'NHA', 'NSK', 'WAW', 'IAR', 'TAS', 'DMM', 'PMY', 'PEE', 'KGS', 'NAV', 'PNS', 'GOI', 'SZG', 'EAS', 'DPS', 'BRC', 'MLE', 'NYC', 'ZCO', 'JED', 'KIN', 'PEZ', 'LIS', 'CMB', 'MIL', 'KUT', 'HEL', 'CPC', 'OMS', 'JNX', 'SGN', 'RTW', 'UBN', 'CLT', 'SJO', 'MCX', 'LPA', 'KUL', 'TPA', 'FAE', 'DHG', 'ELH', 'DOD', 'KVR', 'PLS', 'PTY', 'MIR', 'ZAD', 'BQS', 'MAD', 'SKG', 'BFS', 'ORL', 'SWF', 'UUS', 'TOF', 'DOM', 'DOH', 'SIN', 'DJE', 'MVD', 'MPM', 'MDZ', 'VRN', 'HTA', 'IZO', 'MMY', 'SHJ', 'CHS', 'FNC', 'TZX', 'ELP', 'RVN', 'JNB', 'BJS', 'RMI', 'MAN', 'PDL', 'MUC', 'AUS', 'ZNZ', 'SIT', 'PVK', 'BTS', 'YHZ', 'WUH', 'RAI', 'SUV', 'IAS', 'GZP', 'PEN', 'RGK', 'HGH', 'HKT', 'KGL', 'MQM', 'PLZ', 'SJD', 'PAS', 'LCA', 'SZK', 'VOG', 'KZN', 'MMK', 'SDR', 'NAN', 'PRG', 'TCI', 'ONT', 'YEA', 'BIO', 'GVA', 'COR', 'FEZ', 'CHQ', 'OVS', 'YFC', 'RUH', 'TDX', 'OVD', 'ALA', 'UTP', 'OLB', 'CUR', 'MSY', 'NTE', 'YVA', 'RAK', 'PRN', 'WDH', 'GHV', 'SEA', 'BCN', 'CPH', 'BOD', 'TRD', 'SCW', 'FDF', 'AJA', 'GIB', 'HAJ', 'ASF', 'SFO', 'PVR', 'CFU', 'GAN', 'MIA', 'ADD', 'LOP', 'LXR', 'CCU', 'MNL', 'IND', 'LBJ', 'BTK', 'NCL', 'ECN', 'GUA', 'ISU', 'NBO', 'TIM', 'BOS', 'ATH', 'HAV', 'ELS', 'HKG', 'DEL', 'GOA', 'PFO', 'MOW', 'URA', 'SPK', 'RMF', 'HOU', 'MES', 'RZH', 'SKP', 'BOO', 'NQN', 'URT', 'URJ', 'REK', 'IBZ', 'BKK', 'HMA', 'VCE', 'INI', 'XMN', 'DYG', 'MEL', 'OPO', 'AGA', 'EIN', 'CMN', 'PUS', 'ANK', 'SCV', 'ULY', 'SIA', 'KOA', 'IWA', 'PHS', 'OAJ', 'NZG', 'TMM', 'MLA', 'SEZ', 'LJU', 'ZAG', 'ACE', 'DAD', 'BEG', 'RHO', 'CAG', 'TQO', 'LXA', 'PMI', 'LRM', 'IPC', 'LAX', 'HNL', 'PPT', 'ALC', 'SSH', 'KOS', 'LYS', 'DAR', 'CEI', 'MPH', 'MCT', 'RIO', 'RMO', 'OSL', 'AYT', 'VLC', 'KJA', 'DUB', 'KYA', 'NOZ', 'SUF', 'BIA', 'OKI', 'NAS', 'TMC', 'AHB', 'HRG', 'ASR', 'WAS', 'GRJ', 'NJC', 'BRE', 'BAX', 'SHA', 'CJM', 'RDU', 'SAC', 'BNA', 'AQP', 'NOS', 'JAI', 'HDY', 'SMS', 'AGP', 'FAT', 'OKA', 'URC', 'BHX', 'MTY', 'FKB', 'TLE', 'RZV', 'ARH', 'HDS', 'WVB', 'REU', 'BDS', 'NVT', 'AUH', 'LPB', 'SYD', 'GDN', 'AKL', 'VNO', 'VTE', 'AOJ', 'BOG', 'TRN', 'CEK', 'DIL', 'SAN', 'LEJ', 'NEI', 'LKN', 'RMZ', 'ROR', 'TJM', 'FLR', 'SDQ', 'ALG', 'AMS', 'BUE', 'OVB', 'SLL', 'KPO', 'SCQ', 'SKX', 'PSA', 'BOB', 'BRI', 'HAM', 'HIJ', 'JUL', 'TBS', 'SLZ', 'RGN', 'SGC', 'BLL', 'SVX', 'JMK', 'BJV', 'SLA', 'YMQ', 'ULH', 'ASU', 'CCS', 'USH', 'DBV', 'BWN', 'RRG', 'GZT', 'KUN', 'PSS', 'MDE', 'DIY', 'CEB', 'CLJ', 'YVR', 'ORK', 'WLG', 'FPO', 'PTP', 'NAP', 'OIT', 'IJK', 'NGO', 'DXB', 'FAO', 'GLA', 'YKS', 'LVI', 'KBV', 'SLC', 'BOM', 'RTM', 'SDJ', 'LON', 'PMO', 'POZ', 'BOI', 'MDL', 'YWG', 'CTU', 'DKR', 'LUX', 'CLY', 'RUN', 'WRO', 'MEX', 'BLQ', 'USM', 'ADZ', 'ALY', 'SOQ', 'KWL', 'SXB', 'DFW', 'IGD', 'ROM', 'PKC', 'UPG']
main_cities = ['LED', 'MOW', 'AER', 'DXB']

months = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
    }

months_rus = {
    'Январь': '01',
    'Февраль': '02',
    'Март': '03',
    'Апрель': '04',
    'Май': '05',
    'Июнь': '06',
    'Июль': '07',
    'Август': '08',
    'Сентябрь': '09',
    'Октябрь': '10',
    'Ноябрь': '11',
    'Декабрь': '12'
    }

reverse_months = dict(zip([i for i in months.values()],[i for i in months_rus.keys()]))
session = requests.Session()
URL = 'http://api.travelpayouts.com/v1/prices/calendar'
#Заголовки для сессии
session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (HTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
#Telebot токен
#Вставьте сюда свой токен
token = None

# Файл с базой данных, большинство из них используется, как оперативная память
database_name = 'my_database.db'
shelve_name = 'shelve.db'
status_name = 'shelve2.db'
choose_date = 'choose_date.db'
preparing_date = 'preparing_date.db'
choose_city_name = 'choose_city.db'
choose_month_name = 'choose_month.db'
choose_leave_date = 'choose_data.db'
choose_arrive_date = 'choose_arrive.db'
choose_current_city_name = 'choose_current_city.db'
last_choice_user = 'last_choice_user.db'
current_price_ticket = 'current_price_ticket.db'
condition_choice_date = 'condition_choice_date.db'
update_id_status = 'update_id_status.db'
db_file = "Mydatabase.vdb"

#Ссылки на фотографии городов, спарсенные с сайта
url_photo = ['https://avatars.mds.yandex.net/get-ydo/4393845/2a0000018f71aa07a7ec3ecf31044fa8bb63/diploma','https://cdn.culture.ru/images/88a0e8fa-74e3-5880-ba16-b875262abab7','https://avatars.mds.yandex.net/get-altay/200322/2a0000015b1966be12f3a7f557be8bba62de/XXL_height','https://cdn.tripster.ru/thumbs2/34ae8f2e-6cee-11ee-952d-dad32add1efe.1600x900.jpeg?width=1200&height=630']
photo_city = dict(zip(main_cities,url_photo))
"""
Парсим iso Российских городов в двух режимах
'city_iso' - возвращает словарь, где ключи - это название городов кириллицей,а значения: iso Российских городов
'iso_city' - возвращает словарь, где ключи - это iso Российских городов, а значения: название городов кириллицей
"""
decode_city_iso = find_iso_and_city("city_iso")
decode_city_iso['Дубай'] = "DXB"
decode_city_iso['Псков'] = "PKV"
decode_iso_city = find_iso_and_city("iso_city")
decode_iso_city['DXB'] = "Дубай"
decode_iso_city['PKV'] = "Псков"

#Словари для представления месяцев в различном виде
decode_month = dict(zip(["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],[i for i in months.keys()]))
code_month = dict(zip([i for i in months.keys()],["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]))

class States(Enum):
    """
    в БД Vedis хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_MONTH = "1"
    S_ENTER_CITY = "2"
    S_SET_PRICE = "3"
    S_ENTER_PRICE = "4"
    S_ENTER_TYPE = "5"
    S_ENTER_CURRENT_CITY = "6"
    S_ENTER_URL="7"
    S_ENTER_DATE = "8"
    S_ENTER_DAYS = "9"
    S_ENTER_LAST_CITY = "10"

