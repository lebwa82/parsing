import requests
from bs4 import BeautifulSoup
import csv


#URL = 'https://quotes.toscrape.com/'
URL = 'https://prodoctorov.ru/moskva/sportivnyy-vrach/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0', 'accept': '*/*'}
file = "file123.csv"




def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="b-doctor-card")
    #print("items = ", items)
    doctors=[]

    for item in items:
        doctors.append(
            {
                "name": item.find("span", class_="b-doctor-card__name-surname").get_text(strip=True),
                "experience": item.find("div", class_="b-doctor-card__experience-years").get_text(strip=True),
                "category": item.find("div", class_="b-doctor-card__category").get_text(strip=True),
                #"clinic_name": item.find("span", class_="b-select__trigger-main-text"),
                #"address": item.find("span", class_="b-select__trigger-adit-text")
                #"specialization": item.find("div", class_="b-doctor-card__spec").get_text(strip=True)

            }

        )

    return doctors


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Имя', 'Опыт', 'Категория'])
        for item in items:
            writer.writerow([item['name'], item['experience'], item['category']])




html = get_html(URL)
if html.status_code == 200:
    #print(html.text)
    print("200")
    doctors=get_content(html.text)
    #print(doctors)
    save_file(doctors, file)
else:
    print('Error')



