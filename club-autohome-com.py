# -*- coding: utf-8 -*-
import sys
import requests
import re
import math
import time
import datetime
from lxml import etree
import xlsxwriter as wx
# from dateutil import relativedelta
import random
import os

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

def checkPostPage(xmldata):
    if(len(getRowNodes(xmldata))>0):
        return False
    else:
        return True

def getRowNodes(xmldata):
    data = xmldata
    rownodes=data.xpath('.//div[@class="clearfix contstxt outer-section"]')
    if len(rownodes)==0:
        raise NameError('Can not parse RowNodes!')
    return rownodes
    
def parsePosterName(rownode):
    node=rownode.xpath('.//li[@class="txtcenter fw"]')
    if len(node)==0:
        raise NameError('Can not parse PosterName!')
    node = node[0].xpath('string(.)').strip()
    return node

def parseContent(rownode):
    node=rownode.xpath('.//div[@class="w740"]//text()')
    if len(node)==0:
        node = rownode.xpath('.//div[@class="x-reply font14"]//text()')
    if len(node)==0:
        raise NameError('Can not parse Content!')
    content = '\r\n '.join(node)
    return content

def parsePosterURL(rownode):
    node=rownode.xpath('.//li[@class="txtcenter fw"]/a[1]/@href')
    if len(node)==0:
        node = rownode.xpath('.//li[@class="txtcenter fw"]/a[0]/@href')
    if len(node)==0:
        return None

    return node[0]


def parseFloor(rownode):
    node=rownode.xpath('.//a[@class="rightbutlz fr"]')
    if len(node)==0:
        node = rownode.xpath('.//div[@class="fr"]/a')
    if len(node)==0:
        raise NameError('Can not parse Floor!')
    elif len(node) ==1:
        floor = node[0].xpath('string(.)')
    elif len(node)==2:
        floor =  node[1].xpath('string(.)')
    # floor=re.search("write\('(.*)'\)",floor).group(1)
    return floor

def parsePosterID(url):
    if url ==None:
        return None
    if re.search('cn/(\d+)/home.ht',url):
        return re.search('cn/(\d+)/home.ht',url).group(1)

def parseDateOfPost(rownode):
    node=rownode.xpath('.//span[@xname="date"]')

    if len(node)==0:
        raise NameError('Can not parse DateOfPost!')
    node = node[0].xpath('string(.)')
    # node=re.search("write\('(.*)'\)",node).group(1)
    node=parseDateStr(parseDate(node))
    return node
   
def parseSinglePostRow(rownode):
   
    posterName=parsePosterName(rownode)
    dateOfPost=parseDateOfPost(rownode)
    content=parseContent(rownode)
    posterURL=parsePosterURL(rownode)
    floor=parseFloor(rownode)
    posterID=parsePosterID(posterURL)
    subject=theSubject
    threadURL=theThreadUrl
    isTopicPost= 1 if floor==u'楼主' else 0
    pageNum=theCurrentPage

    node=[theSiteid,subject,content,dateOfPost,floor,posterName,posterURL,posterID,threadURL,isTopicPost,pageNum]
    return node

def parseSinglePostPageAndNeedTurnToNext(xmldata):
    ret=False
    if checkPostPage(xmldata):
        raise NameError('This Page is not a Post Page')
    nodes=getRowNodes(xmldata)

    for node in nodes:
        post=parseSinglePostRow(node)
        if parseDateStrToStamp(post[3])>= parseDateStrToStamp(theDateFilter):
            postdata.append(post)
            print('save a record successfully !')
        

    return True if getNextPageNode(xmldata)[0] ==1 else False

def getNextPageNode(xmldata):
    node=xmldata.xpath('.//a[@class="afpage"]')
    if len(node)==0:
        return 0,0
    # for i in node:
    #     tmp=i.xpath('text()')
    #     if '下一页' in tmp[0]:
    #         pagenode=i
    #         break
    node = node[0].xpath('@href')[0]
    node = "http://club.autohome.com.cn/bbs/" +node
    return 1,node

def turnToPage(url):
    print(url)
    # t=random.uniform(1, 3)
    time.sleep(4)
    res=requests.get(str(url))
    xmldata=res.text
##    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
##    xmldata=res.text.translate(non_bmp_map)
    return xmldata

def getExcel(data):
    title=['siteid','subject','content','dateOfPost','floor','posterName','posterURL','posterID','threadURL','isTopicPost','pageNum']
    
    filename=str(theSiteid)+'_'+str(time.strftime('%Y-%m-%d %H-%M-%S',time.localtime()))
    workbook = wx.Workbook(filename+'.xlsx')
    worksheet = workbook.add_worksheet()

    for i in range(len(data)):
        for j in range(len(title)):
            if i==0:
                worksheet.write(i, j, title[j])
            worksheet.write(i+1, j, data[i][j])
    workbook.close()

 
def doCapture(siteid,threadurl,subject,datefilter):
    global theThreadUrl,theSubject,theDateFilter,theCurrentPage,postdata,theSiteid
    theThreadUrl=threadurl
    theSubject=subject
    theDateFilter=parseDateStr(parseDate(datefilter))
    theCurrentPage=1
    postdata=[]
    errCode=0
    theSiteid=1001

    try:
        print ('start loadPage:'+theThreadUrl)
        res=requests.get(theThreadUrl)
        xmldata=res.text
        xmldata = etree.HTML(xmldata)
        while (parseSinglePostPageAndNeedTurnToNext(xmldata)):
            print ("Turn to next page")
            hasNextPage,pageNode = getNextPageNode(xmldata)
            if hasNextPage==0:
                break
            theCurrentPage +=1
            xml = turnToPage(pageNode)
            xmldata = etree.HTML(xml)
        
        getExcel(postdata)
    except Exception as err:
        errCode=1
        print ('have an error while spidering')
        print(err)
    finally:
        print('Finish Spidering')
        return errCode,postdata



doCapture(1000,'http://club.autohome.com.cn/bbs/thread-c-266-51693908-1.html','subject','2015-07-07 09:33:43')

if __name__ == '__main__':

    CurrentPath = os.getcwd()
    configtext_filepath=os.path.dirname(CurrentPath)+'\ConfigText'
    if os.path.exists(configtext_filepath)==False:
        raise NameError("Don't Exsit ConfigText")
    configtext_path=configtext_filepath+'\ConfigText.txt'
    if os.path.isfile(configtext_path)==False:
        raise NameError("Don't Exsit ConfigText.txt")
    f = open(configtext_path,'rb')
    lines = f.readlines()
    for  line in lines:
        doCapture_para=line.decode().strip('\n').split('@gigi@')
        print('==========')
        print(doCapture_para)
        doCapture(doCapture_para[0],doCapture_para[1],doCapture_para[2],doCapture_para[3])
    f.close()
