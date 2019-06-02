##Script Name: MUNI37MasterSwitch.py
##Author: Trey Landsburg
##Date 5/30/19
##PURPOSE: This script tells the user the best way to reach San Francisco's downtown area from the residential area of 925 Corbett Ave.
##using the BeautifulSoup and pybart.api libraries. This script is intended to evenutally be used with a Raspberry Pi.

##Libraries##
from bs4 import BeautifulSoup
import requests
import time
from pybart.api import BART

bart = BART() ##makes a BART API
root = bart.stn.stninfo('24th')
station = root.find('stations').find('station')
# print(station.find('address').text + ', ' + station.find('city').text)

root_etd = bart.etd.etd('24th',dir='n')
# station_minutes = root_etd.find('station').find('etd').find('estimate').findall('minutes')
# station_destination = root_etd.find('station').find('etd').find('destination')
#
# print(station_destination.text)
# print(station_minutes.text)

bart_destination=[]
bart_minutes=[]
for i in root_etd.find('station').findall('etd'):
    station_destination = i.find('destination').text
    station_minutes = i.find('estimate').find('minutes').text
    station_color = i.find('estimate').find('color').text

    bart_destination.append(station_destination)
    bart_minutes.append(station_minutes)
# print(bart_destination, bart_minutes)

# print(station_etd.find('estimate').find('minutes').text)


t_end = time.time() + 60 * 15
while time.time() < t_end:
    #Arrival Information Feeds#
    source37 = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=37&s=4169&useShortTitles=true').text
    source48 = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=48&s=3463&useShortTitles=true').text
    sourceK = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=K&s=5728&useShortTitles=true').text
    sourceL = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=L&s=5728&useShortTitles=true').text
    sourceM = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=sf-muni&r=M&s=5728&useShortTitles=true').text

    bart=requests.get("https://www.bart.gov/schedules/eta?stn=24TH").text
    # print(bart)

    ##BeautifulSoup##
    soup37=BeautifulSoup(source37,'xml')
    arrivaltime37=soup37.find_all('prediction')

    soup48=BeautifulSoup(source48,'xml')
    arrivaltime48=soup48.find_all('prediction')

    soupK = BeautifulSoup(sourceK, 'xml')
    arrivaltimeK = soupK.find_all('prediction')
    soupL = BeautifulSoup(sourceL, 'xml')
    arrivaltimeL = soupL.find_all('prediction')
    soupM = BeautifulSoup(sourceM, 'xml')
    arrivaltimeM = soupM.find_all('prediction')

    print('**WELCOME TO UPPER MARKET**')

    arrival_list37 = []
    arrival_list48 = []
    arrival_listK = []
    arrival_listL = []
    arrival_listM = []
    for tag in arrivaltime37:
        arrival_list37.append(int(tag.get('minutes')))
    if arrival_list37[0]<5:
        print("The next 37 Corbett is arriving SOON:", arrival_list37[0], "minutes.")
    else:
        print("The next 37 Corbett will arrive in",arrival_list37[0], "minutes.")

    for tag in arrivaltime48:
        arrival_list48.append(int(tag.get('minutes')))
    if arrival_list48[0]<5:
        print("The next 48 Quintara is arriving SOON:", arrival_list48[0], "minutes.")
    else:
        print("The next 48 Quintara will arrive in",arrival_list48[0], "minutes.")

    # for tag in arrivaltimeK:
    #     arrival_listK.append(int(tag.get('minutes')))
    #     prin(arrival_listK)
    for tag in arrivaltimeL:
        arrival_listL.append(int(tag.get('minutes')))
    for tag in arrivaltimeL:
        arrival_listM.append(int(tag.get('minutes')))

    next37=arrival_list37[0]
    next48 = arrival_list48[0]
    # nextK = arrival_listK[0]
    nextL = arrival_listL[0]
    nextM = arrival_listM[0]

    print("*********")

    ##find good connections
    ##travel time to heavy rail: 7 mins via 37 Corbett, 11 via 48 Quintara

    nextL_at_arrival=nextL-7
    nextM_at_arrival = nextM-7
    # print(nextL_at_arrival)
    # print(nextM_at_arrival)

    # bart_minutes_at_arrival1=bart_minutes[0]-11
    # bart_minutes_arrival2 = bart_minutes[1]-11
    # print(bart_minutes_at_arrival1)
    # print(bart_minutes_arrival2)

    if next37<next48:
        print("Fastest way to downtown is currently via the 37 Corbett.")
        print("Transfer at Castro Station to Subway Lines:","L Taraval in",nextL,"minutes","(",nextL_at_arrival,"at arrival)", "OR " "M Ocean View in", nextM, "minutes.""(",nextM_at_arrival,"at arrival)")
    else:
        print("Fastest way to downtown from this location is via the 48 Quintara")
        print("Transfer at 24th St. Station to Subway Lines:","BART TOWARDS:",bart_destination[0], bart_minutes[0],
              bart_destination[1], bart_minutes[1])
    time.sleep(20)
