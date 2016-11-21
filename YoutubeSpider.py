# -*- coding:utf-8 -*-
import os
import sys
import time
import datetime
import requests
import re
import json

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
from selenium.webdriver.common.keys import Keys #引入keys类操作

#from pyquery import PyQuery as pyq
from lxml import etree
import xlsxwriter as wx

reload(sys)
sys.setdefaultencoding('utf8')

class ClassWeb:
    def __init__(self,profile=None):
        self.profile=profile
        self.myBrowser=None
        

    def initWeb(self):

        if(self.profile ==None):
            self.myBrowser=webdriver.Firefox()
        else:
            pro=webdriver.FirefoxProfile(self.profile)
            self.myBrowser=webdriver.Firefox(pro)

    def loadPage(self,url,flag):
        if flag==1:
            self.myBrowser.get(url)
            htmlsource = self.myBrowser.page_source
        else:
            # js="var q=document.documentElement.scrollTop=2000"
            # self.myBrowser.execute_script(js)
            time.sleep(3)
            try:
                print  self.myBrowser.find_element_by_class_name("load-more-text")
                self.myBrowser.find_element_by_class_name("load-more-text").click()
                htmlsource = self.myBrowser.page_source
            except Exception as err:
                return None

        return htmlsource

    def  close(self):
        self.myBrowser.close()


def doCapture(siteId, forumRefineKey, forumId, forumURL, lastScraptTime):
    global theSiteID,theForumID,theLastScraptTime,theForumRefineKey,pagenum,theForumUrl,threaddata,thePoster
    theSiteID= siteId
    theForumID = forumId
    theLastScraptTime = time.strptime(lastScraptTime, "%Y-%m-%d")
    theForumRefineKey = forumRefineKey
    theForumUrl=forumURL
    pagenum=1
    threaddata=[]

    url =forumURL

    try:
        print("start loadpage for url: " + url)

        classweb =ClassWeb()
        classweb.initWeb()
        html_source=classweb.loadPage(url,1)
        html_source = etree.HTML(html_source)
        thePoster =parsePoter(html_source)
        #result = etree.tostring(html_source)
        #print result

        hasNextPageNode = True

        while(hasNextPageNode):
            lastdate,nodelen = parseSingleThreadPage(html_source,pagenum)
            if(nodelen==0):
                break
            pagenum=pagenum+1
            if time.strptime(lastdate, "%Y-%m-%d") < theLastScraptTime :
                break
            html_source = classweb.loadPage(url,pagenum)
            if html_source== None:
                break
            else:
                html_source = etree.HTML(html_source)

            
##            if(nextPageNode<theLastScraptTime):
##                hasNextPageNode=False
##            print(threaddata)
##            if(hasNextPageNode):
##                xml = turnToNextThreadPage(nextPageNode)
            
##        print(threaddata)
        print('start get excel')
        getExcel(threaddata)
        classweb.close()
    except Exception as err:
        print(err)

    finally:
        print('Done')

def parseSingleThreadPage(xmldata,pagenum):
    print("starting parseSingleThreadPage pagenum = "+str(pagenum))
    nodes =getThreadRowNodes(xmldata,pagenum)
    if nodes==None:
        return None,0
    for i in nodes:
        thread = parseSingleThreadRow(i)
        if time.strptime(thread[2], "%Y-%m-%d") >= theLastScraptTime:
            threaddata.append(thread)
    return thread[2], len(nodes)
    # print etree.tostring(i)
    print len(nodes)

        
def getThreadRowNodes(html_source,num):
    print('starting getThreadRowNodes')
    htmldata = html_source.xpath("//li[@class ='channels-content-item yt-shelf-grid-item']")
    print('getThreadRowNodes done ')
    return htmldata
   # realnode=None
    #try:
     #   for i in range(12*num-11,num*12+1):
      #      if i==(12*num-11):
      #          realnode=pyq(rownode.eq(i-1))
     #       else:
      #          realnode=realnode+pyq(rownode.eq(i-1))
     #   print('getThreadRowNodes done')
    #    return realnode
   # except :
     #   return None


    
def parseSingleThreadRow(rownode):
    threadurl=parseThreadUrl(rownode)
    Subject=parseSubject(rownode)
    dateofpost=parseDateOfPost(rownode)
    poster=thePoster
    posterurl=theForumUrl

    singlenode=[threadurl,Subject,dateofpost,poster,posterurl]
    print('parseSingleThreadRow done')
    return singlenode


def parseThreadUrl(rownode):
    try:
        videourl = rownode.xpath('*//a[@class ="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2"]//@href')
        return 'http://www.youtube.com'+ str(videourl)
    except:
        videourl =None
        return videourl



def parseSubject(rownode):
    try:
            subject=rownode.xpath('*//a[@class ="yt-uix-sessionlink yt-uix-tile-link  spf-link  yt-ui-ellipsis yt-ui-ellipsis-2"]//text()')
            return subject[0]
    except:
        subject=None
        return subject


def parsePoter(html_source):
    try:
        poster= html_source.xpath('*//span[@class ="qualified-channel-title-text"]/a[1]//text()')
        return poster[0]
    except:
        poster=None
        return poster


def get_text(nodes):
    return [unicode(node.xpath('text()')[0]) for node in nodes]


def parseDateOfPost(rownode):
        dateofpost = rownode.xpath('*//ul[@class ="yt-lockup-meta-info"]//li[2]')
        s = get_text(dateofpost)[0]
        print s.decode('utf8')
        # print  unicode(dateofpost[0]).decode('utf8')
        # print  dateofpost[0].__str__()
        # print  dateofpost[0]).unicode()text_content().encode('utf-8')
        flat = re.search('(\d+)年',s.decode('utf8'))
        try:
            num=flat.group(1)
            if (num  > 1):
               return "2014-02-01"
            else:
                return "2015-02-01"
        except:
             return "2015-02-01"

def getExcel(data):
    title=['threadurl','subject','dateofpost','poster','posterurl']
    poster=re.search(r'user\/(.*)\/videos',theForumUrl)
    name=poster.group(1)
    workbook = wx.Workbook(name+'.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(len(data)):
        for j in range(len(title)):
            if i==0:
                worksheet.write(i, j, title[j])
            worksheet.write(i+1, j, data[i][j])


doCapture(12, 'forumRefineKey', 'forumId', 'https://www.youtube.com/user/SHISEIDOHK/videos', '2016-10-01')
