from bs4 import BeautifulSoup
import requests
import time

# ##BeautifulSoup
# soup=BeautifulSoup(source,'xml')
# print(soup)
# # print(soup.prettify())

t_end = time.time() + 60 * 15
while time.time() < t_end:
    source = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=37&s=4169&useShortTitles=true').text
    ##BeautifulSoup
    soup=BeautifulSoup(source,'xml')
    print(soup)
    # print(soup.prettify())

    arrivaltime=soup.find_all('prediction')
    # print(type(arrivaltime))
    # print(arrivaltime)
    arrival_list=[]
    for tag in arrivaltime:
        arrival_list.append(int(tag.get('minutes')))
    if arrival_list[0]<5:
        print("The next 37 Corbett is arriving SOON:", arrival_list[0], "minutes.")
    else:
        print("The next 37 Corbett will arrive in",arrival_list[0], "minutes.")
    time.sleep(20)
