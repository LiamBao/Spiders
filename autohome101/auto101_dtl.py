# -*- coding: utf-8 -*-
import re, ctypes,requests,random,os,json,ctypes,win32ui,sys,math,time,datetime

from lxml import etree
import xlsxwriter as wx
from colorFont import Color
from dateParse import *


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

def getThreadNodes(xmldata):
    data = xmldata
    rownodes=data.xpath('.//div[@id ="subcontent"]/dl[@class="list_dl "]')
    if len(rownodes)==0:
        raise NameError('Can not parse threadNodes!')

    # for i in rownodes:
    #     print(i[0].xpath('string(.)').strip())
    return rownodes



def getRowNodes(xmldata):
    data = xmldata
    rownodes=data.xpath('.//div[@class="clearfix contstxt outer-section"]')
    if len(rownodes)==0:
        raise NameError('Can not parse RowNodes!')
    return rownodes
    

def getNextThreadPageNode(xmldata):

    node=xmldata.xpath('.//a[@class="afpage"]')
    if len(node) == 0:
        return None
    node = node[0].xpath('@href')[0]
    return node



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
    content = '\r\n '.join(node).strip().replace('\n','')
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
   
def parseSinglePostRow(rownode,theThreadUrl,theSubject):

    posterName=parsePosterName(rownode)
    dateOfPost=parseDateOfPost(rownode)
    content=parseContent(rownode)
    posterURL=parsePosterURL(rownode)
    floor=parseFloor(rownode)
    posterID=parsePosterID(posterURL)
    subject= theSubject
    threadURL=theThreadUrl
    isTopicPost= 1 if floor==u'楼主' else 0
    pageNum=1
    theSiteid =1000

    node=[theSiteid,subject,content,dateOfPost,floor,posterName,posterURL,posterID,threadURL,isTopicPost,pageNum]
    return node

def getExcel(data):
    title=['siteid','subject','content','dateOfPost','floor','posterName','posterURL','posterID','threadURL','isTopicPost','pageNum']
    try:
        filename='Autohome101_'+str(time.strftime('%Y-%m-%d %H-%M-%S',time.localtime()))
        workbook = wx.Workbook(filename+'.xlsx')
        worksheet = workbook.add_worksheet()

        for i in range(len(data)):
            for j in range(len(title)):
                if i==0:
                    worksheet.write(i, j, title[j])
                worksheet.write(i+1, j, data[i][j])
        workbook.close()
        print('excel Done')
    except Exception as err:
        print("excel "+err)

def getNextPageNode(xmldata):
    node=xmldata.xpath('.//a[@class="afpage"]/@href')
    if len(node)==0:
        return None
    node = node[0].strip()
    return node


def turnToPage(url):
    # t=random.uniform(1, 3)
    # time.sleep(2)
    res=requests.get(url).text
    return res