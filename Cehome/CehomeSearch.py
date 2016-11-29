# -*- coding: utf-8 -*-
import re,requests,random,win32ui,sys,math,threading,time

from lxml import etree
from colorFont import Color
from dateParse import *
from cehome_dtl import  *

__author__ ='liam'
__version__ = 'v2.0'


def postParse(urls):

    global postData
    thepostCurrentPage=1

    for  url2parse in urls:
        try:
            print ('start loadPage: '+ url2parse)
            res = requests.get(theKeywordThreadUrl, timeout = 20)
            xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')
            xmldata = etree.HTML(xmldata)
            subject = parseSubject(xmldata)
            while (parseSinglePostPageAndNeedTurnToNext(xmldata,subject,url2parse)):
                thepostCurrentPage += 1
                print ("Turn to next postPage "+str(thepostCurrentPage))
                pageNode = getNextPostPageNode(xmldata)
                if not pageNode :
                    break
                xmldata = turnTopostPage(pageNode)

        except Exception  as err:
                print ('Has an error while spidering')
                print(err)
        finally:
                print('Finish Spidering')

def threadStart(threadurl):
        list_thread=[]
        threadnum = math.ceil(len(threadurl)/10)
        for i in range(0,len(threadurl),threadnum):
           list_thread.append(threadurl[i:i+threadnum])

        threads = []
        for i in list_thread:
           threads.append(threading.Thread(target=postParse,args=(i,)))

        print('==== start in threading ====')
        for t in threads:
           t.setDaemon(True)
           t.start()

        for t in threads:
          t.join()
        print('====  threading end ====')

def doCapture(keyword):

    clr = Color()
    global threadurl,postData
    theKeywordThreadUrl = "http://search.cehome.com/cse/search?q="+keyword+"&p=0&s=2289651421703031038&nsid=5"
    theCurrentPage=1
    threadurl = []

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

            # if len(threadurl)  > 200:
            #     for url in threadurl:
            #         if url.find('thread') < 0:
            #             continue
            #         postParse(url)
            #     threadurl =[]

            xml = turnToPage(pageNode)
            xmldata = etree.HTML(xml)

        # for url in threadurl:
        #     postParse(url)
        threadStart(threadurl)

        clr.print_green_text('counts ' + str(len(postData)) + '  posts')
        # if len(postData) > 20000:
        #     getExcel(postData)
        #     postData = []

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
    clr.print_green_text('##  Date    11/10/2016')
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

    while True:
        postDateTime = input('请输入抓取截止日期 (格式：2016-1-1): ')
        if postDateTime and re.search('^\d{4}-\d{1,2}-\d{1,2}$',postDateTime):
            break
        else:
            clr.print_red_text("时间错误，请重新输入谢谢！")
            postDateTime = ''

    
    count = 0
    postData = []
    try:

        with open(filename,'rb') as task_lines:
            for 3 in task_lines:
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
        getExcel(postData)
    except Exception as err:
        clr.print_red_text(err)

if __name__ == '__main__':
    main()