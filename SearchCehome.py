# -*- coding: utf-8 -*-
##__author__ =='liam'
import re
import requests
import random
import os
import json
import ctypes
import win32ui
import sys
import math
import time
import datetime
from lxml import etree
import xlsxwriter as wx
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

    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print (print_text)
        self.reset_color()

    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print (print_text)
        self.reset_color()

def parseDate(datestr):
##    print(datestr)
    if re.search('(\d+).*天[之|以]?前',datestr):
        tmp=re.search('(\d+).*天[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(days = int(tmp)))
    elif re.search('(\d+).*日[之|以]?前',datestr):
        tmp=re.search('(\d+).*日[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(days = int(tmp)))
    elif re.search('(\d+).*周[之|以]?前',datestr):
        tmp=re.search('(\d+).*周[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+).*秒[钟]?[之|以]?前',datestr):
        tmp=re.search('(\d+).*秒[钟]?[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(seconds = int(tmp)))
    elif re.search('(\d+).*分钟[之|以]?前',datestr):
        tmp=re.search('(\d+).*分钟[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(minutes = int(tmp)))
    elif re.search('(\d+)个?.*星期[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*星期[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+)个?.*礼拜[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*礼拜[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(weeks = int(tmp)))
    elif re.search('(\d+)个?.*小时[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*小时[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*钟头[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*钟头[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*钟点[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*钟点[之|以]?前',datestr).group(1)
        date_pa = (datetime.datetime.now() - datetime.timedelta(hours = int(tmp)))
    elif re.search('(\d+)个?.*月[之|以]?前',datestr):
        tmp=re.search('(\d+)个?.*月[之|以]?前',datestr).group(1)
        date_pa = datetime.datetime.now() - relativedelta.relativedelta(months = int(tmp)) 
    elif re.search('(\d+).*年[之|以]?前',datestr):
        tmp=re.search('(\d+).*年[之|以]?前',datestr).group(1)
        date_pa = datetime.datetime.now() - relativedelta.relativedelta(years = int(tmp))       
    elif re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}',datestr):
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d %H:%M:%S")
    elif re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}',datestr):
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d %H:%M")
    elif  re.search('\d{4}-\d{1,2}-\d{1,2}',datestr): 
        tmp=re.search('\d{4}-\d{1,2}-\d{1,2}',datestr).group()
        date_pa=time.strptime(tmp, "%Y-%m-%d")
    elif  re.match('.*今.*天.*',datestr):
        today = datetime.date.today()
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(today)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(today), "%Y-%m-%d")
    elif re.match('.*昨.*天.*',datestr):
        day = datetime.date.today()- datetime.timedelta(days=1) 
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(day)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(day), "%Y-%m-%d")
    elif re.match('.*前.*天.*',datestr):
        day = datetime.date.today()- datetime.timedelta(days=2) 
        if re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr):
            tmp=re.search('\d{1,2}:\d{1,2}:\d{1,2}',datestr).group()
            date_pa=time.strptime(str(day)+' '+tmp, "%Y-%m-%d %H:%M:%S")
        else:
            date_pa=time.strptime(str(day), "%Y-%m-%d")
    return date_pa

def parseDateStr(date_pa):
    return time.strftime("%Y-%m-%d %H:%M:%S", date_pa)

def parseDateStrToStamp(datestr):
       return time.mktime(time.strptime(datestr,'%Y-%m-%d %H:%M:%S'))


def parseinputDateStrToStamp(datestr):
    return time.mktime(time.strptime(datestr, '%Y-%m-%d '))

def checkThreadPage(xmldata):
    if(len(getThreadNodes(xmldata))>0):
        return False
    else:
        return True

def checkPostPage(xmldata):
    if(len(getRowNodes(xmldata))>0):
        return False
    else:
        return True

def getRowNodes(xmldata):
    data = xmldata
    rownodes=data.xpath('.//div[@id="postlist"]/div/table')

    # contains:.//a[contains(@class,'btnX') and .//text()='Sign in']
	# starts-with：.//a[starts-with(@class,'btnSelectedBG')]

    if len(rownodes)==0:
        raise NameError('Can not parse post RowNodes!')
    return rownodes

def getThreadNodes(xmldata):
    data = xmldata
    rownodes=data.xpath('.//div[@class="result f s0"]')
    if len(rownodes)==0:
        raise NameError('Can not parse threadNodes!')

    # for i in rownodes:
    #     print(i[0].xpath('string(.)').strip())
    return rownodes
    
def parsePosterName(rownode):
    node=rownode.xpath('.//div[@class="authi"]/a')
    if len(node)==0:
        raise NameError('Can not parse PosterName!')
    node = node[0].xpath('string(.)').strip()
    return node

def parseContent(rownode):
    node=rownode.xpath('.//td[@class="t_f"]//text()')
    if len(node)==0:
        node = rownode.xpath('.//div[@class="t_fsz"]//text()')
    if len(node)==0:
        raise NameError('Can not parse Content!')
    content = ' '.join(node)
    return content

def parsePosterURL(rownode):
    node=rownode.xpath('.//div[@class="authi"]/a/@href')
    if len(node)==0:
        node = rownode.xpath('.//li[@class="txtcenter fw"]/a[0]/@href')
    if len(node)==0:
        return None

    return node[0]


def parseFloor(rownode):
    node=rownode.xpath('.//div[@class ="pi"]/strong/a')
    if len(node)==0:
        raise NameError('Can not parse Floor!')
    elif len(node) ==1:
        floor = node[0].xpath('string(.)')

    # floor=re.search("write\('(.*)'\)",floor).group(1)
    return floor

def parsePosterID(url):
    if url ==None:
        return None
        
    if re.search('space-uid-(\d+).html',url):
        return re.search('space-uid-(\d+).html',url).group(1)

def parseDateOfPost(rownode):

    node=rownode.xpath('.//div[@class="authi"]/em')

    if len(node)==0:
        raise NameError('Can not parse DateOfPost!')
    node = node[0].xpath('string(.)').replace('发表于 ','')
    # node=re.search("write\('(.*)'\)",node).group(1)
    node=parseDateStr(parseDate(node))
    return node
   
def parseSinglePostRow(rownode,thesubject,url2parse):
    global  thepostCurrentPage
    posterName=parsePosterName(rownode)
    dateOfPost=parseDateOfPost(rownode)
    content=parseContent(rownode)
    posterURL=parsePosterURL(rownode)
    floor=parseFloor(rownode)
    posterID=parsePosterID(posterURL)
    subject=thesubject
    threadURL=url2parse
    isTopicPost= 1 if floor==u'楼主' else 0
    pageNum = thepostCurrentPage

    node = [1111,subject,content,dateOfPost,floor,posterName,posterURL,posterID,threadURL,isTopicPost,pageNum]
    return node

def parseSinglePostPageAndNeedTurnToNext(xmldata,subject,url2parse):
    global  postDateTime,postData
    if checkPostPage(xmldata):
        raise NameError('This Page is not a Post Page!')
    nodes = getRowNodes(xmldata)

    for node in nodes:
        post=parseSinglePostRow(node,subject,url2parse)

        if parseDateStrToStamp(post[3]) >= parseinputDateStrToStamp(postDateTime):
            postData.append(post)
            print('save a record successfully !')
    return True if getNextPostPageNode(xmldata) != None else False



def  parseSingleThreadPageAndNeedTurnToNext(xmldata):
    global threadurl 
    if checkThreadPage(xmldata):
        raise NameError('This Page is not a thread Page')
    nodes = getThreadNodes(xmldata)
    for node in nodes:
        url = node.xpath('.//a[@target="_blank"]/@href')
        url = url[0].strip()
        threadurl.append(url)
    return True if  getNextThreadPageNode(xmldata) != None  else False

def getNextThreadPageNode(xmldata):

    node=xmldata.xpath('.//a[@class="pager-next-foot n"]')
    if len(node) == 0:
        return None
    node = node[0].xpath('@href')[0]
    return node


def getNextPostPageNode(xmldata):
    node=xmldata.xpath('.//div[@class = "pg"]/a[@class ="nxt"]')
    if len(node)==0:
        return None
    node = node[0].xpath('@href')[0]
    return node



def turnToPage(url):

    res = requests.get(str(url), timeout=10)
    xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')
    return xmldata

def turnTopostPage(url):

    # waitTime=random.uniform(1, 2)
    # time.sleep(waitTime)
    res = requests.get(str(url), timeout=10).text
    return res


def parseSubject(xmldata):

    subject = xmldata.xpath('.//td[@class = "ptm pbn"]/div[@class = "ts z h1"]')
    subject  =subject[0].xpath('string(.)').strip().replace('[复制链接]','')
    return subject


def postParse(url2parse):

    global postData,thepostCurrentPage
    thepostCurrentPage=1

    try:
        print ('start loadPage: '+ url2parse)
        res=requests.get(url2parse,timeout = 20).text
        xmldata = etree.HTML(res)
        subject = parseSubject(xmldata)
        while (parseSinglePostPageAndNeedTurnToNext(xmldata,subject,url2parse)):
            thepostCurrentPage += 1
            print ("Turn to next postPage "+str(thepostCurrentPage))
            pageNode = getNextPostPageNode(xmldata)
            if not pageNode :
                break
            xml = turnTopostPage(pageNode)
            xmldata = etree.HTML(xml)
        
    except Exception as err:
        errCode=1
        print ('Has an error while spidering')
        print(err)
    finally:
        print('Finish Spidering')


def doCapture(keyword):

    clr = Color()
    global threadurl,postData,postFlag
    theKeywordThreadUrl = "http://search.cehome.com/cse/search?q="+keyword+"&p=0&s=2289651421703031038&nsid=5"
    theCurrentPage=1

    try:

        res = requests.get(theKeywordThreadUrl, timeout = 20)
        xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')
        xmldata = etree.HTML(xmldata)
        while (parseSingleThreadPageAndNeedTurnToNext(xmldata)):
            print (" Turn to next  threadPage : "+str(theCurrentPage))
            theCurrentPage += 1
            if theCurrentPage > 74:
                break
            if  not getNextThreadPageNode(xmldata):
                break
            pageNode = "http://search.cehome.com/cse/"+getNextThreadPageNode(xmldata)            

            if len(threadurl)  > 200 and postFlag == 1:
                for url in threadurl:
                    if url.find('thread') < 0:
                        continue
                    postParse(url)
                    # waitTime = random.uniform(1, 2)
                    # clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
                    # time.sleep(waitTime)
                threadurl =[]

            xml = turnToPage(pageNode)
            xmldata = etree.HTML(xml)
        if postFlag == 1 :
            for url in threadurl:
                postParse(url)
                # waitTime = random.uniform(1, 2)
                # clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
                # time.sleep(waitTime)
            clr.print_green_text('counts ' + str(len(postData)) + '  posts')
        if len(postData) > 20000:
            getExcel(postData)
            postData = []

    except Exception as err:
        print ('has an error while spidering')
        print(err)
    finally:
        print('Finish Spidering')


def main():

    global clr,postData,postDateTime
    clr = Color()
    clr.print_green_text('*'*40)
    clr.print_green_text('##  Python  3.4')
    clr.print_green_text('##  Author  Liam')
    clr.print_green_text('##  Date   11/10/2016')
    clr.print_green_text('##  Crawl   CehomeSearch')
    clr.print_green_text('*'*40)

    clr.print_green_text('Enter to Open File')
    dlg = win32ui.CreateFileDialog(1)   # 表示打开文件对话框
    dlg.SetOFNInitialDir('C:/')  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()
    clr.print_green_text('Open File or directory: '+filename)
    # f = open(os.getcwd()+r'/indexCrawl.txt','rb')
    if filename is None or filename == '':
       sys.exit(0)

    postDateTime = input("请输入抓取截止日期：(格式如 2016-01-01)")

    count = 0
    postData = []
    data =[]


    try:

        with open(filename,'r') as task_lines:
            for line in task_lines:
                try:
                    count += 1
                    line = str(line, encoding='utf-8')
                    line = line.strip()
                    
                    if not line:
                        continue
                    clr.print_green_text('Start Parsing keyword : '+str(line))
                    doCapture(line)
                    clr.print_green_text('Keyword: '+line+ ' parsing Done!')
                    waitTime = random.uniform(3, 5)
                    clr.print_green_text("  wait for "+str(int(waitTime))+" Seconds!")
                    time.sleep(waitTime)
                except Exception as err:
                    clr.print_red_text (err)

    except Exception as err:
        clr.print_red_text(err)


def getExcel(data):
    clr = Color()
    try:
        title = ['siteid','subject','content','dateOfPost','floor','posterName','posterURL','posterID','threadURL','isTopicPost','pageNum']

        file_name = '%s%s' % ('Output_',("%d" % (time.time() * 1000)))
        
        workbook = wx.Workbook(file_name+'.xlsx')
        worksheet = workbook.add_worksheet('post')
        for i in range(len(data)):
            for j in range(len(title)):
                if i==0:
                    worksheet.write(i, j, title[j])
                worksheet.write(i+1, j, data[i][j])

        workbook.close()
        clr.print_green_text('\n File '+file_name+' Done!')   
    except Exception as err:
        clr.print_red_text(err)


if __name__ == '__main__':
    main()