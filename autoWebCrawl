# -*- coding: utf-8 -*-
import re
import requests
import math
import time
import datetime
from lxml import etree
import xlsxwriter as wx
import random
import os
import json
import ctypes 


STD_INPUT_HANDLE = -10  
STD_OUTPUT_HANDLE= -11  
STD_ERROR_HANDLE = -12  
  
FOREGROUND_BLACK = 0x0  
FOREGROUND_BLUE = 0x01 # text color contains blue.  
FOREGROUND_GREEN= 0x02 # text color contains green.  
FOREGROUND_RED = 0x04 # text color contains red.  
FOREGROUND_INTENSITY = 0x08 # text color is intensified.  
  
BACKGROUND_BLUE = 0x10 # background color contains blue.  
BACKGROUND_GREEN= 0x20 # background color contains green.  
BACKGROUND_RED = 0x40 # background color contains red.  
BACKGROUND_INTENSITY = 0x80 # background color is intensified.  
  
class Color:  
    ''''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp 
    for information on Windows APIs.'''  
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)  
      
    def set_cmd_color(self, color, handle=std_out_handle):  
        """(color) -> bit 
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY) 
        """  
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)  
        return bool  
      
    def reset_color(self):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)  
      
    def print_red_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)  
        print (print_text)  
        self.reset_color()
    def print_green_text(self, print_text):  
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)  
        print (print_text)  
        self.reset_color() 




def parseCar(siteType,pageHtml):

        if (siteType == 2):
            car = pageHtml.xpath('//div[@class ="infor_my_box"]/p/a')
            if len(car) == 0:
                return " "
            else:
                car =car[0].xpath('string(.)')
        elif (siteType == 3):
            car = pageHtml.xpath('//h3[@class ="user-name"]')
            if car == None:
                return " "
            else:
                car = car[0].xpath('string(.)')

        return car


def parsePoter(siteType,pageHtml):
    if(siteType == 1):
        PosterName =pageHtml.xpath('//h3[@class ="user-name"]')
        if len(PosterName) == 0:
            return " "
        else:
            PosterName = PosterName[0].xpath('string(.)')
            PosterName = PosterName.replace(' ', '')
    elif (siteType == 2):
        PosterName =pageHtml.xpath('//h4[@id ="avatar_title"]/strong')
        if len(PosterName) == 0:
            return " "
        else:
            PosterName =PosterName[0].xpath('string(.)')
    elif (siteType == 3):
        PosterName =pageHtml.xpath('//h1[@class ="user-name"]/b')
        if len(PosterName) == 0:
            return " "
        else:
            PosterName = PosterName[0].xpath('string(.)')

    return  PosterName


def parseLevel(siteType,pageHtml):
    if(siteType == 1):
        Level =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if len(Level) == 0:
            return " "
    elif (siteType == 2):
        Level =pageHtml.xpath('//div[@class ="middle_box_ta"]/ul/li[1]')
        if len(Level) == 0:
            return " "
        else:
            Level = Level[0].xpath('string(.)')
            Level = Level.replace('等级：','')
    elif (siteType == 3):
        pass
    return  Level



def parsenumOfThreads(siteType,pageHtml):
    if(siteType == 1):
        numOfThreads =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if numOfThreads == None:
            return "numOfThreads"
    elif (siteType == 2):
        numOfThreads =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if numOfThreads == None:
            return "numOfThreads"
    elif (siteType == 3):
        numOfThreads =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if numOfThreads == None:
            return "numOfThreads"

    return  numOfThreads



def parseLocation(siteType,pageHtml):
    if(siteType == 1):
        Location =pageHtml.xpath('//span[@class ="muted"][2]')
        if len(Location) == 0:
            return " "
        else:
            Location = Location[0].xpath('string(.)')
            Location = Location.replace('地区:', '')
    elif (siteType == 2):
        Location =pageHtml.xpath('//div[@class ="middle_box_ta"]/ul/li[2]')
        if len(Location) == 0:
            return " "
        else:
            Location =Location[0].xpath('string(.)')
            Location = Location.replace('地区：','')
    elif (siteType == 3):
        Location =pageHtml.xpath('//a[@class ="state-pos"]')
        if len(Location) == 0:
            return " "
        else:
            Location = Location[0].xpath('string(.)')
            Location = Location.replace('所在地','')

    return  Location



def parseFans(siteType,pageHtml):
    if(siteType == 1):
        fans =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if len(fans) == 0:
            return " "
    elif (siteType == 2):
        fans =pageHtml.xpath('//div[@class ="middle_box_ta"]/ul/li[7]')
        if len(fans) == 0:
            return " "
        else:
            fans = fans[0].xpath('string(.)')
            fans = fans.replace('粉丝：','')
    elif (siteType == 3):
        fans =pageHtml.xpath('//div[@class ="user-lv"]/a[3]/span')
        if len(fans) == 0:
            return " "
        else:
            fans = fans[0].xpath('string(.)')

    return  fans



def parseFollowing(siteType,pageHtml):
    if(siteType == 1):
        following =pageHtml.xpath('//h3[@class ="user-name"]//text()')
        if len(following) == 0:
            return " "
    elif (siteType == 2):
        following =pageHtml.xpath('//div[@class ="middle_box_ta"]/ul/li[5]')
        if len(following) == 0:
            return " "
        else:
            following = following[0].xpath('string(.)')
            following = following.replace('关注：','')
    elif (siteType == 3):
        following =pageHtml.xpath('//div[@class ="user-lv"]/a[2]/span')
        if len(following) == 0:
            return " "
        else:
            following = following[0].xpath('string(.)')
    return  following


def main_pcauto(mainLists):
    site = 'Pcauto.com'
    siteType = 1
    clr = Color()
    global errorCount,errorUrls
    try:

        url = re.search(r'pcauto.com.cn/(\d+)', mainLists)
        if url:
            print("Start parsing Url :  " + mainLists)
            PosterID =url.group(1)
            url = "http://my."+str(url.group(0))
        else:
            print("请输入符合类型的 Url: " + mainLists)
##            pcautoExit=input('Enter to continue')
            errorCount += 1
            errorUrls.append(mainLists)
            return None

        pageHtml = requests.get(url,timeout = 20).text

        nowTime = "%d" % (time.time() * 1000)
        if pageHtml.find('title>的主页')>0 or pageHtml.find('asd') >0:
            errorCount += 1
            errorUrls.append(mainLists)
            clr.print_red_text('Invalid Page!')
            return None
        else:
            carID = re.search(r'carAttr(\d+)',str(pageHtml))
            if  carID == None:
                print("Cant parse CarID!")
                car = " "
            else:
                carID = re.search(r'carAttr(\d+)', str(pageHtml)).group(1)
                carUrl = "http://my.pcauto.com.cn/intf/getCarAttr.jsp?callback=jsonp"+nowTime+"&act=getCarAttr&carId="+carID
                car_jsonHtml = requests.get(carUrl).text
                if car_jsonHtml is None:
                    car = None
                else:
                    if (re.search(r'{(.*)}', car_jsonHtml)) != None:
                        car_jsonHtml = re.search(r'({.*})', car_jsonHtml).group(1)
                        car = json.loads(car_jsonHtml)
                        car = "Series :" + car['series'] + " Brand :" + car['brand'];

        followingurl = "http://my.pcauto.com.cn/bip/intf/focus.jsp?act=getFocusNum&accountId=" +PosterID+ "&callback=jsonp"+nowTime
        fanurl = "http://my.pcauto.com.cn/bip/intf/focus.jsp?act=getFocusByNum&accountId=" +PosterID+ "&callback=jsonp"+nowTime

        follow_jsonHtml = requests.get(followingurl).text
        if follow_jsonHtml ==  None:
            follow = ' '
        else:
            if ( re.search(r'\((\d+)\)\;',follow_jsonHtml) ) != None:
                follow = re.search(r'\((\d+)\)\;',follow_jsonHtml).group(1)

        fan_jsonHtml = requests.get(fanurl).text
        if fan_jsonHtml ==  None:
            follow = ' '
        else:
            if ( re.search(r'\((\d+)\)\;',fan_jsonHtml) ) != None:
                fan =re.search(r'\((\d+)\)\;',fan_jsonHtml) .group(1)

        pageHtml = etree.HTML(pageHtml)
        PosterName = parsePoter(siteType,pageHtml)
        posterUrl = url
        Level = 'Null'
        numOfThreads = 'Null'    #parsenumOfThreads(siteType, pageHtml)
        Location = parseLocation(siteType, pageHtml)
        fans = fan  #parseFans(siteType, pageHtml)
        following = follow  #parseFollowing(siteType, pageHtml)

        threads = [site,PosterName,posterUrl,PosterID,car,Level,numOfThreads,Location,fans,following]
        clr.print_green_text('parsing succesfully!')
        yield  threads
    except Exception as err:
        print(err)


def main_yiche(mainLists):
    site = 'yiche.com'
    siteType = 2
    clr = Color()
    global errorCount,errorUrls
    try:
 
        url = re.search(r'yiche.com/u(\d+)', mainLists)
        if url:
            print("Start parsing Url :  " + mainLists)
            PosterID =url.group(1)
            url = "http://i.yiche.com/u"+str(url.group(1))
        else:
            print("请输入符合类型的 Url: " + mainLists)
##            yicheExit = input('Enter to continue!')
            errorUrls.append(mainLists)
            errorCount += 1
            return None

        headers = {
            'Host': 'i.yiche.com',
            'Referer': 'http://baa.bitauto.com/qicheyanghu/thread-9563506.html',
            'Upgrade-Insecure-Requests': '1',
            'User - Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        try:
            pageHtml = requests.get(url,headers = headers,timeout = 20).text

            if(pageHtml.find('error/Awarderror')>0 ):
                clr = Color()
                clr.print_red_text('Invalid Page!')
                errorCount += 1
                errorUrls.append(mainLists)
                return None
            pageHtml = etree.HTML(pageHtml)
        except :
            errorCount += 1
            errorUrls.append(mainLists)
            print ('Invalid PageUrl')

        car = parseCar(siteType,pageHtml)
        PosterName = parsePoter(siteType,pageHtml)
        posterUrl = url
        Level = parseLevel(siteType,pageHtml)
        numOfThreads = 'Null'      #parsenumOfThreads(siteType, pageHtml)
        Location = parseLocation(siteType, pageHtml)
        fans = parseFans(siteType, pageHtml)
        following = parseFollowing(siteType, pageHtml)

        threads = [site,PosterName,posterUrl,PosterID,car,Level,numOfThreads,Location,fans,following]
        clr.print_green_text('parsing succesfully!')
        yield threads
    except Exception as err:
        print(err)



def main_autohome(mainLists):
    site = 'autohome.com'
    siteType = 3
    clr = Color()
    global errorCount,errorUrls
    try:

        url = re.search(r'autohome.com.cn/(\d{1,10})', mainLists)
        if url:
            print("Start parsing Url :  " + mainLists)
            PosterID =url.group(1)
            url = "http://i.autohome.com.cn/"+str(url.group(1))
        else:
            print("请输入符合类型的 Url: " +mainLists)
##            autoExit = input('Enter to continue!')
            errorUrls.append(mainLists)
            errorCount += 1
            return None

        headers = {
            'Host': 'i.autohome.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
            'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',

        }

        try:
           pageHtml = requests.get(url,headers = headers,timeout = 20).text
           if(pageHtml.find('用户不存在') >0 ):
              clr = Color()
              clr.print_red_text('Invalid Page!')
              errorCount += 1
              errorUrls.append(mainLists)
              return None
        except :
            clr = Color()
            clr.print_red_text('Invalid Page!')
            errorCount += 1
            errorUrls.append(mainLists)
            return None

        carUrl = 'http://i.autohome.com.cn/'+PosterID+'/car#pvareaid=104341'
        carHtml = requests.get(carUrl).text

        pageHtml = etree.HTML(pageHtml)
        carHtml = etree.HTML(carHtml)


        PosterName = parsePoter(siteType,pageHtml)
        posterUrl = url
        Level = 'Null'
        numOfThreads = 'Null'
        Location = parseLocation(siteType, pageHtml)
        fans = parseFans(siteType, pageHtml)
        following = parseFollowing(siteType, pageHtml)

        carThreads =carHtml.xpath('//ul[@class="focusCar"]/li')
        if carThreads == None:
            car = ''
            threads = [site,PosterName,PosterID,car,Level,numOfThreads,Location,fans,following]
            return threads
        else:

            for carThread in carThreads:
                carInfo = carThread.xpath('./div[@class ="fcpc"]/strong')
                if len(carInfo) == 0:
                    carInfo = ''
                else:
                    carInfo = carInfo[0].xpath('string(.)')
                certifications = carThread.xpath('./a[@class = "rzcz m_t_3"]')
                if len(certifications) == None:
                    certifications = ''
                else:
                    certifications = '  !认证'

                car = carInfo+certifications
                threads = [site, PosterName,posterUrl, PosterID, car, Level, numOfThreads, Location, fans, following]
                yield  threads

        clr.print_green_text('parsing succesfully!')
    except Exception as err:
        print(err)


def getExcel(data):
    clr = Color()
    try:
        title = ['Site','PosterName','posterUrl','PosterID','carInfo','Level','numOfThreads','Location','fans','following']
        errtitle = ['errorUrl']
        workbook = wx.Workbook('carCrawl'+'.xlsx')
        worksheet = workbook.add_worksheet('carInfo')
        for i in range(len(data)):
            for j in range(len(title)):
                if i==0:
                    worksheet.write(i, j, title[j])
                worksheet.write(i+1, j, data[i][j])

        worksheet = workbook.add_worksheet('errUrl')
        # print ('~'*20)
        # print(str(len(errorUrls)))
        # print(str(len(errtitle)))
        for i in range(len(errorUrls)):
            for j in range(len(errtitle)):
                if i==0:
                    worksheet.write(i, j, errtitle[j])
                worksheet.write(i+1, j, errorUrls[i])

        workbook.close()

    except Exception as err:
        clr.print_red_text(err)

try:

    print('*'*40)
    print('##  Version 1.1')
    print('##  Python  3.4')
    print('##  Author  Liam')
    print('##  Data    2016/08/26')
    print('##  Crawl   CarUserInfo Data')
    print('*'*40)
    print('\r\n')

    time.sleep(1.5)

    f = open(os.getcwd()+r'/carCrawl.txt','rb')
    mainlists = [i for i in f.readlines()]
    f.close()
    count = 0
    threaddata = []
    data =[]
    clr = Color()
    global errorCount,errorUrls
    errorCount =0
    errorUrls =[]

    # 操作Main函数
    for mainlist in mainlists:
        count += 1
        print ("parsing Number : " , count)
                
        if len(mainlist) < 10:
           clr.print_red_text("Invalid Url\r\n")
           errorCount += 1
           continue

        mainlist = str(mainlist,encoding='utf-8')

        if(mainlist.find('pcauto') > 1):
            threaddata = main_pcauto(mainlist)
        elif(mainlist.find('yiche')> 1):
            threaddata = main_yiche(mainlist)
        elif(mainlist.find('autohome') > 1):
            threaddata = main_autohome(mainlist)
        for i in threaddata:
            data.append(i)
            
        waitTime = random.uniform(2, 5)
        print("Wait for "+str(int(waitTime))+" Seconds~")
        time.sleep(waitTime)
        
    # 1:Excel文件：
    getExcel(data)
    clr.print_green_text("\r\nSave Succesfully ")

except Exception as err:
    print(err)

finally:
    clr = Color()
    clr.print_red_text('Counts '+str(errorCount)+' errors')
    clr.print_green_text ("\r\n  DONE")
    exitLine=input('Enter to exit')
    
# version 1.1 ：requests包增加timeout = 20
#
#
#
#
#
#
#
#
#
#
#
#
#
#
