# -*- coding: utf-8 -*-
import re,requests,random,win32ui,sys,math,threading,time

from lxml import etree
from colorFont import Color
from dateParse import *
from cehome_dtl import  *

__author__ ='liam'
__version__ = 'v2.0'

WEB_HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'search.cehome.com',
    # 'Host': 'bbs.cehome.com',
    # 'Referer':'http://search.cehome.com/cse/search?q=%E5%8D%A1%E7%89%B9&click=1&s=2289651421703031038&nsid=5',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}
POST_HEADERS={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host': 'bbs.cehome.com',
    # 'Referer':'http://search.cehome.com/cse/search?q=%E5%8D%A1%E7%89%B9&click=1&s=2289651421703031038&nsid=5',
    # 'Referer': '{url}',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
}

def parseSinglePostPageAndNeedTurnToNext(xmldata,subject,url2parse,thepostCurrentPage):
    global  postDateTime,postData
    if checkPostPage(xmldata):
        raise NameError('This Page is not a Post Page!')
    nodes = getRowNodes(xmldata)
    for node in nodes:
        post=parseSinglePostRow(node,subject,url2parse,thepostCurrentPage)
        if parseDateStrToStamp(parseDateStr(parseDate(post[3]))) >= parseDateStrToStamp(parseDateStr(parseDate(postDateTime))):
            postData.append(post)
            print('save a record successfully !')
    return True if getNextPostPageNode(xmldata) else False



def  parseSingleThreadPageAndNeedTurnToNext(xmldata):
    global threadurl
    if checkThreadPage(xmldata):
        raise NameError('This Page is not a thread Page')
    nodes = getThreadNodes(xmldata)
    for node in nodes:
        url = node.xpath('.//a[@target="_blank"]/@href')
        url = url[0].strip()
        # http://bbs.cehome.com/thread-31175-1-1.html
        if url.find('viewthread')>-1:
            threadurl.append(url)
        elif url.find('cehome.com/thread')>-1:
            if re.search('^http://bbs.cehome.com/thread-\d+-\d+-1.html$',url):
                url  = re.search("^(http://bbs.cehome.com/thread-\d+)-\d+-1.html$",url).group(1)
                url = url+'-1-1.html'
                threadurl.append(url)
    return True if  getNextThreadPageNode(xmldata)  else False



def postParse(urls):
    for  url2parse in urls:
        try:
            thepostCurrentPage = 1
            print ('start loadPage: '+ url2parse)
            try:
                res = requests.get(url2parse, headers =POST_HEADERS ,timeout = 10).text
            except:
                res = requests.get(url2parse, headers=POST_HEADERS, timeout=10)
                res = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')     # 特殊编码
            if not res: raise NameError('Can not get Post requests')
            xmldata = etree.HTML(res)
            subject = parseSubject(xmldata)
            while (parseSinglePostPageAndNeedTurnToNext(xmldata,subject,url2parse,thepostCurrentPage)):
                thepostCurrentPage += 1
                print ("Turn to next postPage "+str(thepostCurrentPage))
                pageNode  = getNextPostPageNode(xmldata)
                xmldata = turnTopostPage(pageNode)
                xmldata = etree.HTML(xmldata)

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
    theKeywordThreadUrl = "http://search.cehome.com/cse/search?q="+keyword+"&p=0&s=2289651421703031038&srt=def&nsid=5"
    theCurrentPage=1
    threadurl = []

    try:

        res = requests.get(theKeywordThreadUrl ,headers  =WEB_HEADERS, timeout = 10)
        xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')
        xmldata = etree.HTML(xmldata)
        while (parseSingleThreadPageAndNeedTurnToNext(xmldata)):
            print (" Turn to next  threadPage : "+str(theCurrentPage))
            theCurrentPage += 1
            if theCurrentPage > 74:
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
        if len(postData) > 20000:
            getExcel(postData)
            postData = []

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
       sys.exit()

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
                    waitTime = random.uniform(2, 4)
                    clr.print_green_text("  wait for "+str(int(waitTime))+" Seconds!")
                    time.sleep(waitTime)
                except Exception as err:
                    clr.print_red_text (err)

        getExcel(postData)
    except Exception as err:
        clr.print_red_text(err)
    finally:
        input('Parse Successfully ! Enter to Exit~')


if __name__ == '__main__':
    main()