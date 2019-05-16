from bs4 import BeautifulSoup
import requests
import time
import re

import matplotlib.pyplot as plt
from numpy.random import rand


# ##BeautifulSoup
# soup=BeautifulSoup(source,'xml')
# print(soup)
# # print(soup.prettify())

source1 = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=37&s=4169&useShortTitles=true').text
source2 = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=sf-muni&r=N&t=1144953500233').text
str(source2)
# print("source1:",source1)

print("source2:",source2)
print(type(source2))
vehicles_ids=(re.findall(r'(?<=vehicle id=)[^.\s]*',source2))
vehicles_lat=(re.findall(r'(?<=lat=)[^\s]*',source2))
vehicles_speed=(re.findall(r'(?<=speedKmHr=")[^"]*',source2))

vehicles_speed_mph=[]
for i in vehicles_speed:
    int(i)*0.621371
    vehicles_speed_mph.append(int(i))

fastest_bus=max(vehicles_speed_mph)
slowest_bus=min(vehicles_speed_mph)

print("The fastest bus on the 37 Corbett is currently going: ",fastest_bus,"mph")
print("The slowest bus on the 37 Corbett is currently going: ",slowest_bus,"mph")


##Scatter Plot option
a = vehicles_ids
b = vehicles_speed
plt.scatter(b, a)
plt.show()
