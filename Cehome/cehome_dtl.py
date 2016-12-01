# -*- coding: utf-8 -*-
import  re,requests,random,time

from lxml import etree
from colorFont import Color
from dateParse import *
import xlsxwriter as wx
from CehomeSearch import WEB_HEADERS

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
    return content.strip().replace('\n','')

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
   
def parseSinglePostRow(rownode,thesubject,url2parse,thepostCurrentPage):

    try:
        posterName=parsePosterName(rownode)
        dateOfPost=parseDateOfPost(rownode)
        content=parseContent(rownode)
        posterURL=parsePosterURL(rownode)
        floor=parseFloor(rownode)
        posterID=parsePosterID(posterURL)
        subject=thesubject
        threadURL = url2parse
        isTopicPost= 1 if floor == u'楼主' else 0
        pageNum = thepostCurrentPage
    except Exception as err:
        print(err)

    node = [1111,subject,content,dateOfPost,floor,posterName,posterURL,posterID,threadURL,isTopicPost,pageNum]
    return node



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
    t=random.uniform(2, 3)
    time.sleep(t)
    try:
        res = requests.get(url, headers=WEB_HEADERS, timeout=10)
        xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')
    except:
        xmldata = requests.get(url, headers=WEB_HEADERS, timeout=10).text
    return xmldata

def turnTopostPage(url2parse):

    t=random.uniform(1, 2)
    time.sleep(t)
    try:
        xmldata = requests.get(url2parse, headers=WEB_HEADERS, timeout=10).text
    except:
        res = requests.get(url2parse, headers=WEB_HEADERS, timeout=10)
        xmldata = res.content.decode('utf-8', 'replace').encode('utf8', 'replace')

    return xmldata


def parseSubject(xmldata):
    subject  =None
    subject = xmldata.xpath('.//td[@class = "ptm pbn"]/div[@class = "ts z h1"]')
    if subject:
        subject  =subject[0].xpath('string(.)').strip().replace('[复制链接]','').replace('\n','')
    return subject


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