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

headerdata = {"authority":"www.facebook.com",
             # "path":"/1theK/videos/807540739293123/",
             "method":"GET",
             "scheme":"https",
             "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             # "accept-encoding":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
             "accept-language":"zh-CN,zh;q=0.8",
             "cache-control":"max-age=0",
             "cookie":"fr=001qiluCrMwjzImYc..BXwBpO.Mc.AAA.0.0.BXwBpO.AWWMzGoz; datr=ihjAV-USp_fW78Avzb3EA5aF; reg_fb_gate=https%3A%2F%2Fwww.facebook.com%2FUrCosme.hk%2Fposts%2F1015600475174314%3FFacebookLikes%3D0%253FFacebookComments%253D0%253FFacebookShares%253D0; reg_fb_ref=https%3A%2F%2Fwww.facebook.com%2F117246628326445%2Fposts%2F1090688127648952%3FFacebookLikes%3D0%253FFacebookComments%253D0%253FFacebookShares%253D0; wd=1440x405",

             "referer":"https://www.facebook.com/",
             "upgrade-insecure-requests":"1",
             "user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
             }


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


def main(mainLists):
    site = 'Facebook.com'
    siteType = 1
    clr = Color()
    global errorCount,errorUrls
    try:

        url = re.search(r'facebook.com/(.*)', mainLists)
        if url :
            print("Start parsing Url :  " + mainLists)
        else:
            clr.print_red_text("请输入符合类型的 Url: " + mainLists)
##            pcautoExit=input('Enter to continue')
            errorCount += 1
            errorUrls.append(mainLists)
            return None

        pageHtml = requests.get(mainLists,headers = headerdata,timeout =20).text
        # pageHtml =pageHtml.encode().decode('utf-8')

##        nowTime = "%d" % (time.time() * 1000)
        if pageHtml.find('{"feedbacktargets":') < 0:
            errorCount += 1
            errorUrls.append(mainLists)
            clr.print_red_text('Invalid Page!')
            return None
        else:
            hasThread = re.search(r'\{"feedbacktargets":\[\{(.*?)\}\]\,',str(pageHtml))
            if  hasThread == None:
                print("Cant parse threads!")
                return None
            else:
                threads =re.search(r'\{"feedbacktargets":\[\{(.*?\})\],\[\]\]',str(pageHtml)).group(0)
                # threads = threads.replace('],[]]','')
                # threads = json.loads(threads)

        hasLikeNum = re.search(r'\"likecount\":(\d+),', threads)
        if hasLikeNum is None:
            likeNum = 0
        else:
            likeNum =hasLikeNum.group(1)


        hasCommentNum = re.search(r'\"commentcount\":(\d+),', threads)
        if hasCommentNum == None:
                comNum = 0
        else:
            comNum =hasCommentNum.group(1)

        hasShareNum = re.search(r'\"sharecount\":(\d+),', threads)
        if hasShareNum == None:
            shareNum =0
        else:
            shareNum =hasShareNum.group(1)




        threads = [mainLists,likeNum,comNum,shareNum]
        clr.print_green_text('parsing succesfully!')
        yield  threads
    except Exception as err:
        print(err)


def getExcel(data):
    clr = Color()
    try:
        title = ['mainLists','likeNum','comNum','shareNum']
        errtitle = ['errorUrl']
        workbook = wx.Workbook('indexCrawl'+'.xlsx')
        worksheet = workbook.add_worksheet('indexInfo')
        for i in range(len(data)):
            for j in range(len(title)):
                if i==0:
                    worksheet.write(i, j, title[j])
                worksheet.write(i+1, j, data[i][j])

        worksheet = workbook.add_worksheet('errUrl')

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
    print('##  Version 1.0')
    print('##  Python  3.4')
    print('##  Author  Liam')
    print('##  Data    2016/08/30')
    print('##  Crawl   FacebookIndex ')
    print('*'*40)
    print('\r\n')

    time.sleep(1)

    f = open(os.getcwd()+r'/indexCrawl.txt','rb')
    mainlists = [i for i in f.readlines()]
    f.close()
    count = 0
    threaddata = []
    data =[]
    clr = Color()
    global errorCount ,errorUrls
    errorCount = 0
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

        if(mainlist.find('facebook') > 1):
            threaddata = main(mainlist)
        # elif(mainlist.find('yiche')> 1):
        #     threaddata = main_yiche(mainlist)
        # elif(mainlist.find('autohome') > 1):
        #     threaddata = main_autohome(mainlist)
        for i in threaddata:
            data.append(i)
            
        # waitTime = random.uniform(2, 5)
        # print("Wait for "+str(int(waitTime))+" Seconds...")
        # time.sleep(waitTime)
        
    # 1:Excel文件：
    getExcel(data)
    clr.print_green_text("\r\nSave Succesfully ")

except Exception as err:
    print(err)

finally:
    clr = Color()
    clr.print_red_text('Counts '+str( errorCount )+' errors')
    clr.print_green_text ("\r\n  DONE")
    exitLine=input('Enter to exit ')
