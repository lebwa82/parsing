from itertools import count
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


#URL = 'https://quotes.toscrape.com/'
URL = 'https://prodoctorov.ru/moskva/sportivnyy-vrach/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0', 'accept': '*/*'}
file = "file123.csv"
HOST = "https://prodoctorov.ru"
page_number = 1
count_doctors=0



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="b-doctor-card")
    #print("items = ", items)
    doctors=[]
    global count_doctors

    for item in items:
        try:
            url_doctor=item.find("div", class_="b-doctor-card__name").find("a").get("href")
            url_doctor.strip()
            url_doctor=HOST+url_doctor
            #print("url_doctor=", url_doctor)
            html_doctor=get_html(url_doctor)
            soup_doctor = BeautifulSoup(html_doctor.text, 'html.parser')
    

            
            doctor_name = soup_doctor.find("span", class_="b-doctor-intro__title-name").get_text().strip()
            #print(doctor_name)

            city = soup_doctor.find("div", class_="b-doctor-intro__title-sub").get_text().strip()
            #print(city)

            array=[]
            item_specializations = soup_doctor.find_all("a", class_="b-doctor-intro__spec")
            for specialization in item_specializations:
                array.append(specialization.get_text())
            specializations=" ".join(array)
            #print(specializations)

            experience = soup_doctor.find("div", class_="b-doctor-intro__exp").get_text().strip()
            #print(experience)

            degree = soup_doctor.find("div", class_="b-doctor-intro__degree").get_text()
            #print(degree)

            clinic_name=[]
            addres=[]
            metro_list=[]
            array=[]
            clinics = soup_doctor.find_all("div", class_="b-doctor-contacts__wp-block")
            for clinic in clinics:
                clinic_name.append(clinic.find("div", class_="b-doctor-contacts__lpu").find("a").get_text().strip())
                addres.append(clinic.find("div", class_="b-doctor-contacts__lpu-address").get_text().strip())

                array=[]
                metros = clinic.find_all("div", class_="b-doctor-contacts__metro")
                for metro_addres in metros:
                    array.append(metro_addres.find("span", class_="b-doctor-contacts__metro-name").get_text().strip())
                array=" ".join(array)
                metro_list.append(array)      
                
            '''
            feedback = soup_doctor.find('div', class_='reviews-filter')
            print(feedback)
            abc=feedback.find("span")
            print("abc=",abc)
            #print(type(feedback))
            '''

            work=[]
            education=soup_doctor.find('div', id='educations')
            steps = education.find_all('li', class_='b-doctor-details__list-item b-doctor-details__list-item_in-row')
            for step in steps:
                a=step.find("div" , class_='b-doctor-details__list-item-title').get_text().strip()
                b=step.find("div", class_="b-doctor-details__number").get_text().strip()
                s=str(a)+str(b)
                " ".join(s.split())
                #print(s)
                work.append(s)
            #print(work)
            for i in range(2):
                clinic_name.append("")
                addres.append("")
                metro_list.append("")
                work.append("")


            doctors.append(
                {
                    "doctor_name": doctor_name,
                    "city": city,
                    "specializations": specializations,
                    "experience": experience, 
                    "degree": degree,
                    "clinic_name1": clinic_name[0],
                    "addres1": addres[0],
                    "metro1": metro_list[0],
                    "clinic_name2": clinic_name[1],
                    "addres2": addres[1],
                    "metro2": metro_list[1],
                    "clinic_name3": clinic_name[2],
                    "addres3": addres[2],
                    "metro3": metro_list[2],
                    "university": work[0],
                    "apirant": work[1],
                    "ordinator": work[2],
                }

            )
            
            print(count_doctors)
            count_doctors+=1
        
        
        except:# такая конструкция связана с отсутствием у некоторых докторов образования или других важных данных
        #я могу бы проверить, каких данных конкретно нет и вывести соответветствующее сообщение
        #но мне кажется, что на начальном этапе таких "специалистов" стоит просто пропустить
            pass

        




    return doctors




doctors=[]


while(count_doctors<15):
    html = get_html(URL, params={'page': page_number})
    if html.status_code == 200:
        print("200")
        doctors.extend(get_content(html.text, ))
        page_number+=1
frame=pd.DataFrame(doctors)
#print(frame)
writer = pd.ExcelWriter('output.xlsx')
frame.to_excel(writer)
writer.save()
    




