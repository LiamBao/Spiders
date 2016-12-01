# -*- coding: utf-8 -*-
import re,requests,random,win32ui,sys,math,threading

from lxml import etree
from colorFont import Color
from dateParse import *
from auto101_dtl import  *

__author__ ='liam'
__version__ = 'v1.0'


WEB_HEADERS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'club.autohome.com.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}


def parseSinglePostPageAndNeedTurnToNext(xmldata,theThreadUrl,theSubject):
    global postData,postDateTime
    if checkPostPage(xmldata):
        raise NameError('This Page is not a Post Page')
    nodes= getRowNodes(xmldata)

    for node in nodes:
        post=parseSinglePostRow(node,theThreadUrl,theSubject)
        if parseDateStrToStamp(parseDateStr(parseDate(post[3])))>= parseDateStrToStamp(parseDateStr(parseDate(postDateTime))):
            postData.append(post)
            print('save a record successfully !')
    return True if getNextPageNode(xmldata) else False


def  parseSingleThreadPageAndNeedTurnToNext(xmldata):
    global threadurl,postDateTime
    try:
        if checkThreadPage(xmldata):
            raise NameError('This Page is not a thread Page')
        nodes = getThreadNodes(xmldata)
        for node in nodes:
            url = node.xpath('.//a[@class="a_topic"]/@href')
            url = "http://club.autohome.com.cn/"+url[0]
            lastreply = node.xpath('.//span[@class = "ttime"]')[0].xpath('string(.)').strip()
            if parseDateStrToStamp(parseDateStr(parseDate(lastreply))) >=  parseDateStrToStamp(parseDateStr(parseDate(postDateTime))):
                threadurl.append(url)
            else:
                return False
    except Exception as err:
        print(err)
    return True if  getNextThreadPageNode(xmldata) != None  else False



 
def postCapture(url):
    global postData,postDateTime
    theCurrentPage=1
    for  theThreadUrl in url:
        try:
            print ('start loadPostPage:'+theThreadUrl)
            res=requests.get(theThreadUrl,headers = WEB_HEADERS,timeout =10).text
            xmldata = etree.HTML(res)
            theSubject  = xmldata.xpath('.//div[@class ="consnav"]/span[6]')
            theSubject = theSubject[0].xpath('string(.)').strip()
            while (parseSinglePostPageAndNeedTurnToNext(xmldata,theThreadUrl,theSubject)):
                pageNode = "http://club.autohome.com.cn/bbs/" +getNextPageNode(xmldata)
                print ("Turn to next postPage "+pageNode)
                theCurrentPage +=1
                xml = turnToPage(pageNode)
                xmldata = etree.HTML(xml)

        except Exception as err:
            print ('have an error while spidering')
            print(err)


def threadStart(threadurl):
        list_thread=[]
        threadnum = math.ceil(len(threadurl)/10)
        for i in range(0,len(threadurl),threadnum):
           list_thread.append(threadurl[i:i+threadnum])

        threads = []
        for i in list_thread:
           threads.append(threading.Thread(target=postCapture,args=(i,)))

        print('==== start in threading ====')
        for t in threads:
           t.setDaemon(True)
           t.start()

        for t in threads:
          t.join()
        print('====  threading end ====')


def ThreadCapture(url):

    global threadurl,postData,postDateTime
    theCurrentPage=1
    threadurl = []

    try:
        res = requests.get(url, headers = WEB_HEADERS,timeout = 10).text
        xmldata = etree.HTML(res)
        while (parseSingleThreadPageAndNeedTurnToNext(xmldata)):
            theCurrentPage  += 1
            print (" Turn to next  threadPage : "+str(theCurrentPage))
            pageNode = "http://club.autohome.com.cn"+getNextThreadPageNode(xmldata)      
            xml = turnToPage(pageNode)
            xmldata = etree.HTML(xml)

        threadStart(threadurl)
            # waitTime = random.uniform(1, 2)
            # clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
            # time.sleep(waitTime)
        threadurl = []

        # for one_url in threadurl:
        #     postCapture(one_url)
        #     # waitTime = random.uniform(1, 2)
        #     # clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
        #     # time.sleep(waitTime)
        #     threadurl = []


    except Exception as err:
        print ('has an error while spidering')
        print(err)
    finally:
        print('Finish Spidering')


def main():

    global postDateTime,postData
    clr = Color()
    clr.print_green_text('*'*40)
    clr.print_green_text('##  Python  3.4')
    clr.print_green_text('##  Author  Liam')
    clr.print_green_text('##  Date    11/25/2016')
    clr.print_green_text('##  Crawl   Autohome101')
    clr.print_green_text('*'*40)

    clr.print_green_text('Enter to Open File')
    dlg = win32ui.CreateFileDialog(1)   # 表示打开文件对话框
    dlg.SetOFNInitialDir('C:/')   # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()
    clr.print_green_text('Open File : '+filename)

    if filename is None or filename == '':
       sys.exit(0)


    while True:
        postDateTime = input('请输入抓取截止日期 (格式：2016-1-1):')
        if postDateTime and re.search('^\d{4}-\d{1,2}-\d{1,2}$',postDateTime):
            postDateTime = postDateTime
            break
        else:
            clr.print_red_text("时间格式错误，请重新输入谢谢！")
            postDateTime = ''

    # postCrawlFlag = input('是否抓取评论(Y/N)')
    # if postCrawlFlag == '' or (not postCrawlFlag):
    #     sys.exit(0)
    # elif: postCrawlFlag == 'Y' or postCrawlFlag == 'y':
    #     postCrawlFlag = 1   #抓取评论
    # elif: postCrawlFlag == 'N' or postCrawlFlag == 'n':
    #     postCrawlFlag = 0   #不抓取评论
    postData = []
    count = 0
    try:
        with open(filename,'rb') as task_lines:
            for line in task_lines:
                try:
                    count += 1
                    line = str(line, encoding='utf-8')
                    line = line.strip()
                    if not line or line.find('type=101')<0 or line.find('club.autohome.com') <0:
                        continue
                    clr.print_green_text('Start parsing forumUrl : '+str(line))
                    ThreadCapture(line)
                    clr.print_green_text('Url: '+str(line)+ ' parsing Done!')
                    t = random.uniform(2, 4)
                    clr.print_green_text("threadCapture  Wait for "+str(int(t))+" Seconds!")
                    time.sleep(t)
                    if len(postData) > 20000:
                        clr.print_green_text('Counts ' + str(len(postData)) + '  posts')
                        getExcel(postData)
                        postData = []
                        waitTime = random.uniform(3, 5)
                        clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
                        time.sleep(waitTime)
                except Exception as err:
                    clr.print_red_text (err)
            if postData:
                clr.print_green_text('Counts ' + str(len(postData)) + '  posts')
                getExcel(postData)

    except Exception as err:
        clr.print_red_text(err)
    finally:
        input('Enter to exit ')


if __name__ == '__main__':
    main()