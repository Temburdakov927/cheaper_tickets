import requests
from bs4 import BeautifulSoup


s = requests.Session()
all_city_photos = 'all_city_photos.db'
URL = 'https://aviakassir.info/tools/citycode/country.html?country=RU&ysclid=m63sj4go1f891774494'
#URL = "https://phototowns.ru/all/"
s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
headers = {
    'Host': 'hh.ru',
    'Connection': 'keep-alive',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    #'max_redirects': '50'
}


def find_iso_and_city(kind_job):
    iso_city = {}
    r = s.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table",{'style':"border:1px solid #000000; width: 100%;text-transform: uppercase;"})
    row = table.find_all("tr")
    for counter,td in enumerate(row):
        td = td.find_all("td")
        towns = []
        for town in td:
            if '\xa0' in town.text:
                town = town.text.replace(' \xa0', '')
            else:
                town = town.text
            towns.append(town)
        if counter >= 2:
            if kind_job == 'iso_city':
                iso_city[towns[1]] = towns[2]
            elif kind_job == 'city_iso':
                iso_city[towns[2]] = towns[1]

    return iso_city


def find_photo_city_2(url):

    #URL_PHOTO_CITY =  f'https://phototowns.ru/{city}/'
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    container_photo = soup.find("div",{'class':"gallery"})
    try:
        photo = container_photo.find("a")
        return photo['href']
    except:
        print(url)


def find_photo_city_3():
    import utils
    URL_PHOTO_CITY = "https://phototowns.ru/all/"
    city_photo = {}
    r = s.get(URL_PHOTO_CITY)
    soup = BeautifulSoup(r.text, 'html.parser')
    container_photo = soup.find_all("div",{'style':"width: 200px; height: 300px; float: left; margin: 10px;"})
    for element in container_photo:
        h2 = element.find("h2")
        site = h2.find("a")
        city_name = h2.text
        city_name_clean = city_name.split(" ")[0]
        photo = find_photo_city_2(site['href'])
        city_photo[city_name_clean] = photo
        utils.set_user_game(city_name_clean, photo, all_city_photos)
    return city_photo
