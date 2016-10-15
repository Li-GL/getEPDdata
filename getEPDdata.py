#-*- coding:utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import os
import csv
from collections import deque
import time

#//////////////////////////////get data per hour//////////////////////////////#
def getRealTimeData(url):
# ------------------------------beautifulsoup------------------------------#
    opener = urllib.urlopen(url)
    html = opener.read()
    opener.close()
    soup = BeautifulSoup(html,'lxml')

    #get monitoring station
    stationHTML = repr(soup.findAll('div',attrs="tilNormal"))
    station = BeautifulSoup(stationHTML,'lxml').div.string
    station = station.replace('/',' ')
    #get latest time
    timeHTML = repr(soup.findAll('td',attrs="H24C_ColDateTime"))
    latestTime = BeautifulSoup(timeHTML,'lxml').td.string
    latestTime = latestTime.replace('\\xa0',' ')
    #get lastest data
    data = soup.findAll('td',attrs="H24C_ColItem")
    dataList = [BeautifulSoup(repr(i),'lxml').td.string for i in data[:6]]

#------------------------------write to csv------------------------------#
    current_path = os.getcwd()
    save_path = os.path.join(current_path, 'AtmosphereData',station)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file= latestTime[0:10] + '_' + station + '.csv'
    filename = os.path.join(save_path,file)
    # write header
    if not os.path.exists(filename):
        with open(filename,'w') as csvfile:
            fieldnames = ['Datetime', 'NO2(ug/m3)', 'O3(ug/m3)', 'SO2(ug/m3)', 'CO(ug/m3)', 'PM10(ug/m3)', 'PM2.5(ug/m3)']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
            writer.writeheader()
    #check datetime, if the data exist, return, no writing to csv
    with open(filename, 'r') as f:
         lastTime = deque(csv.reader(f), 1)[0][0]
    if lastTime == latestTime:
        return 0
    #write data
    with open(filename, 'a') as csvfile:
        fieldnames = ['Datetime', 'NO2', 'O3', 'SO2', 'CO', 'PM10', 'PM2.5']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'Datetime': latestTime, 'NO2': str(dataList[0]), 'O3':str(dataList[1]),\
                         'SO2': str(dataList[2]), 'CO': str(dataList[3]), 'PM10': str(dataList[4]),\
                         'PM2.5': str(dataList[5])})
    returnData = str(latestTime)  + '   '+ 'NO2: '+str(dataList[0]) +'   '+ 'O3: ' + str(dataList[1])+ '   '+\
                         'SO2: ' + str(dataList[2])  + '   '+ 'CO: ' + str(dataList[3])  + \
           '   ' + 'PM10: ' + str(dataList[4]) + '   ' +'PM2.5: ' + str(dataList[5]) + '  '+ str(station)
    print returnData

#//////////////////////////////main function//////////////////////////////#

EPDstaionURL  = ['http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration1f2c.html?stationid=70', #Yuen Long 元朗
                'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration45fd.html?stationid=80', #Central/Western 中心区
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentratione1a6.html?stationid=73', #Eastern 东区
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentrationfb71.html?stationid=74', # Kwun Tong 观塘
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentrationdb46.html?stationid=66', # Sham Shui Po 深水埗
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration30e8.html?stationid=72', # Kwai Chung 葵涌
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration228e.html?stationid=77', # Tsuen Wan 荃湾
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration0b35.html?stationid=83', # Tseung Kwan O 将军澳
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration537c.html?stationid=82', # Tuenn Mun 屯门
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentrationf322.html?stationid=78', # Tung Chung 东涌
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration6e9c.html?stationid=69', # Tai Po 大埔
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration2c5f.html?stationid=75', # Sha Tin 沙田
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration233a.html?stationid=76', # Tap Mun 塔门
                  #road side station 路边监测站
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration5ca5.html?stationid=71', #Causeway Bay 铜锣湾
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentrationf9dd.html?stationid=79', #Central 中环
                 'http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration9c57.html?stationid=81' #Mong Kok 旺角
               ]
while True:
    for url in EPDstaionURL:
        try:
            getRealTimeData(url)
        except:
            continue
    time.sleep(600)
