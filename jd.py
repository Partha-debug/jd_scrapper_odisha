places = [
    "Balasore",
    "Bhubaneshwar",
    "Cuttack",
    "Rourkela",
    "Berhampur-Odisha",
    "Sambalpur",
    "Puri",
    "Bhadrak",
    "Jajpur",
    "Mayurbhanj",
    "Khurda",
    "Angul",
    "Dhenkanal"
    ]
business = [
    "Readymade-Garment-Dealers",
    "Textile-Dealers",
    "Restaurants",
    "Cement-Dealers",
    "Steel-Dealers",
    "Paper-Dealers",
    "Automobile-Dealers",
    "Insurance-Companies",
    "Jewellery-Showrooms",
    "Home-Appliance-Dealers",
    "Hotels",
    "Gyms"
    ]


from collections import defaultdict
from logging import exception
from tkinter import OFF
from bs4 import BeautifulSoup
import requests
import tinycss
import pandas as pd


def org_num_finder(stylesheet,orgs_data):

    class_map = []

    for i in stylesheet.rules:
        if i.line == 189:
            if 'content'in str(i.declarations):
                key = i.selector[1].value
                value = int(str(i.declarations[0].value[0]).split()[-1][-3]) -1

                class_map.append((key,value if value != -1 else 9))
                if len(class_map) == 10:
                    break 

    class_map = dict(class_map)

    for org in orgs_data:
        org_phone = org.find_all('span',{'class':'mobilesv'})[::-1][:10][::-1]
        org_num = '+91'
        for element in org_phone:
            org_num+=str(class_map[element.attrs['class'][1]] if element.attrs['class'][1] in class_map.keys() else '*')

        data['Phone'].append(org_num)




def org_name_finder(orgs_data):
    for org in orgs_data:
        org_name = org.find('span', {'class':'lng_cont_name'}).attrs['data-cn']
        data['Organization'].append(org_name)
    
    


for i in places:
    for j in business:
        for k in range(1,40):


            url= f"https://www.justdial.com/{i}/{j}/page-{k}"

            r = requests.get(url=url,headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
            parser = tinycss.make_parser('page3')
            soup = BeautifulSoup(r.content, "html.parser")
            raw_style = parser.parse_stylesheet_bytes(r.content)
            orgs = soup.find_all('div',{'class':'col-sm-5 col-xs-8 store-details sp-detail paddingR0'})
            data = defaultdict(list)
            org_name_finder(orgs)
            org_num_finder(raw_style,orgs)
            print(data)

            df = pd.DataFrame(data)
            df.to_csv(f"{i}_{j}.csv", mode='a', index=False, header=False)


