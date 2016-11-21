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
import win32ui
import threading

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


insheaderdata = {"authority":"www.instagram.com",
             "method":"GET",
             "scheme":"https",
             "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             "accept-language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
             "cache-control":"max-age=0",
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


def face_main(mainLists):
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




def ins_main(mainLists):
    site = 'Instagram.com'
    siteType = 2
    clr = Color()
    global errorCount,errorUrls
    try:

        url = re.search(r'instagram.com/(.*)', mainLists)
        if url :
            print("Start parsing Url :  " + mainLists)
        else:
            clr.print_red_text("请输入符合类型的 Url: " + mainLists)
##            pcautoExit=input('Enter to continue')
            errorCount += 1
            errorUrls.append(mainLists)
            return None
        reTimes = 0
        begin = int(time.time() * 1000)

        while reTimes < 5:
            try:
                pageHtml = requests.get(mainLists, headers=insheaderdata, timeout=10).text
            except:
                try :
                    pageHtml = requests.get(mainLists,timeout=10).text
                except Exception as err:
                    print('requests Again!')
            reTimes += 1
        end = int(time.time() * 1000)
        clr.print_green_text('\n\r\r\r\r\r\rRequets Costs '+str(end-begin)+' ms !')
        if pageHtml is None:
            return None
##        nowTime = "%d" % (time.time() * 1000)
        if pageHtml.find('Sorry, this page isn\'t available.') > 0:
            errorCount += 1
            errorUrls.append(mainLists)
            clr.print_red_text('Invalid Page!')
            return None
        else:
            hasThread = re.search(r'window._sharedData = \{.*?\};', (pageHtml))
            if  hasThread == None:
                print("Cant parse threads!")
                return None
            else:
                threads =re.search(r'window._sharedData = \{.*?\};', (pageHtml)).group(0)
                # threads = threads.replace('],[]]','')
                # threads = json.loads(threads)
        # print (threads)
        hasLikeNum = re.search(r'likes\"\: \{\"count\"\: (\d+),', threads)
        if hasLikeNum is None:
            likeNum = 0
        else:
            likeNum =hasLikeNum.group(1)


        hasCommentNum = re.search(r'comments\"\: \{\"count\"\: (\d+)\,', threads)
        if hasCommentNum == None:
                comNum = 0
        else:
            comNum =hasCommentNum.group(1)

        shareNum = None
        # hasShareNum = re.search(r'\"sharecount\":(\d+),', threads)
        # if hasShareNum == None:
        #     shareNum =0
        # else:
        #     shareNum =hasShareNum.group(1)




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
        file_name = '%s%s' % ('Output_',("%d" % (time.time() * 1000)))
        
        workbook = wx.Workbook(file_name+'.xls')
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




def main():

    try:

        # print('*'*40)
        # print('##  Version 1.0')
        # print('##  Python  3.4')
        # print('##  Author  Liam')
        # print('##  Data    2016/08/30')
        # print('##  Crawl   FacebookIndex ')
        # print('*'*40)
        # print('\r\n')

        print('*'*40)
        print('##  Version 2.0')
        print('##  Python  3.4')
        print('##  Author  Liam')
        print('##  Data    2016/09/19')
        print('##  Crawl   Facebook & Instargram Thread Index ')
        print('*'*40)
        print('\r\n')


        global errorCount,errorUrls,data,count
        errorCount = 0
        count = 0
        errorUrls =[]
        data =[]

        clr = Color()
        clr.print_green_text('Enter to Open File')
        input('')
        dlg = win32ui.CreateFileDialog(1) # 表示打开文件对话框
        dlg.SetOFNInitialDir('C:/') # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        filename = dlg.GetPathName()
        clr.print_green_text('Open File or directory: '+filename)
        # f = open(os.getcwd()+r'/indexCrawl.txt','rb')
        if filename is None or filename == '':
            sys.exit(0)
        f = open(filename,'rb')
        mainlists = [i for i in f.readlines()]
        f.close()
        
        threaddata = []
        data =[]
        
        
        list_thread=[]
##        realthreadnum=threadnum
        threadnum=math.ceil(len(mainlists)/10)
        for i in range(0,len(mainlists),threadnum):
           list_thread.append(mainlists[i:i+threadnum])

        threads = []
        for i in list_thread:
           threads.append(threading.Thread(target=threadMain,args=(i,)))

        print('============== start in threading ==============')
        for t in threads:
           t.setDaemon(True)
           t.start()

        for t in threads:
          t.join()   
            
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



def threadMain(mainlists):
       clr = Color()
       for mainlist in mainlists:
            global errorCount ,errorUrls,data,count
            count += 1
            print ("parsing Number : " , count)
                    
            if len(mainlist) < 10:
               clr.print_red_text("Invalid Url\r\n")
               errorCount += 1
            else:
                mainlist = str(mainlist,encoding='utf-8')
                mainlist = mainlist.strip()
                if(mainlist.find('facebook') > 1):
                    threaddata = face_main(mainlist)
                elif(mainlist.find('instagram')> 1):
                    threaddata = ins_main(mainlist)
                for i in threaddata:
                    data.append(i)
                # waitTime = random.uniform(2, 5)
                # print("Wait for "+str(int(waitTime))+" Seconds...")
                # time.sleep(waitTime)
   

if __name__ == '__main__':
    main()

