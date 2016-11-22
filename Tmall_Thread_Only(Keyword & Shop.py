# -*- coding: utf-8 -*-
# __author__ =='liam'
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



def parseDateStr(date_pa):
    return time.strftime("%Y-%m-%d %H:%M:%S", date_pa)

def parseDateStrToStamp(datestr):
    return time.mktime(time.strptime(datestr,'%Y-%m-%d %H:%M:%S'))


def loadProductList(keyword,pageNum):
    global  clr
    if keyword:
        try:
            valueNode=(pageNum-1)*44
            kstsNode="%d" % (time.time() * 1000)
            headers = { 'cookie' : 'thw=cn; cna=jCGdDgo1eioCAXTsq3pq4acz; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc3=nk2=AnywymvJAg%3D%3D&id2=UoH8VdpejL6PVA%3D%3D&vt3=F8dAScPiFCD1VRRbxcs%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; lgc=amen_nm; tracknick=amen_nm; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=0_1; isg=C5C64B911C2D2BE426E05E1803925CC7; l=AqOjku73WJcR8NeISY45WOfjs-lNqTfa; v=0; cookie2=1cfd2313facba6013b6a051a56edb89b; t=3dc0209d48a7022db36cbc763b2dc39e; _tb_token_=4fGjN8315alJ; linezing_session=05Sk9B4qqJDNTd7AxIiVwFxA_1450151125996X9SX_1; JSESSIONID=A810EE3F9B371ADCC646C7C948F1A11C',
                                     'referer':'https://www.taobao.com/',
                                      'user-agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                    }

            url = "https://s.taobao.com/search?data-key=s&data-value="+str(valueNode)+"&ajax=true&_ksTS="+str(kstsNode)+"_1116&callback=jsonp1117&isprepay=1&initiative_id=staobaoz_20141104&tab=mall&q="+keyword+"&style=list&stats_click=search_radio_tmall%253A1&sort=sale-desc&s="+str(valueNode)

    ##        url = "http://s.taobao.com/search?data-key=s&data-value="+str(valueNode)+"&ajax=true&_ksTS="+str(kstsNode)+"_1341&callback=jsonp1341&sort=sale-desc&initiative_id=staobaoz_"+str(time.strftime("%Y%m%d",time.localtime(time.time())))+"&tab=all&q="+keyword+"&style=list&s="+str(valueNode)
            html = requests.get(url,headers = headers,timeout = 10).text
            return html

        except Exception as err:
            clr.print_red_text(err+'  Cannot parse Page')




def  getJsons(xml,parse_type):
    global theDomain,clr

    if parse_type == 1:
        startPos = xml.find("({")
        if ( startPos > -1):
            jsonStr = xml[startPos+1:len(xml)]
            endPos = jsonStr.find("})")
            jsonStr = jsonStr[0:endPos+1]


        jsonStr = jsonStr.replace("\n", "")
        jsonStr = jsonStr.replace("\r", "")
        jsonStr =  jsonStr.replace("\"cassandre\"", "cassandre")

        try:
            jsons = json.loads(jsonStr)

        except Exception as err:
            print('Parsing Error ON Json')

        return jsons
    
    elif parse_type == 2:
        xml = str(xml)
        part1=xml[0:xml.find("?")+1]
        part2=xml[xml.find("?")+1:]
        # timestamp  = int(time.time())
        # xml=theDomain+part1+'_ksTS='+str(timestamp)+'_658&callback=jsonp659&'+part2
        xml= theDomain+part1+"_ksTS=1434002336091_658&callback=jsonp659&"+part2

        jsonxml = requests.get(xml,timeout = 10).text
        if jsonxml.find("(") >-1:
            startPos = jsonxml.find("(")
            if jsonxml.find("</body>") >-1:
                endPos = jsonxml.find("</body>")
                jsonxml = jsonxml[startPos+1:endPos]
                jsonxml= jsonxml.replace('\\','')
        else:
            jsonxml = None
        return jsonxml


def getNextProductPageNode(string):

    if string.find('J_SearchAsync next') < 0:
        return None

    if string.find('J_SearchAsync next') > -1:
        index = string.find('J_SearchAsync next')
    if string.find('下一页',index) > -1:
        end = string.find('下一页',index)
    string = string[index:end]

    if string.find('href='):
        index=string.find('href=')
    else:
        return None
    string = string[index+7:]
    string = string[0:len(string) - 3]
    return "https:" + string


def parseProductPage(xml):
    global clr,threads
    nextPageNode = None

    # 判断该页面是否一个有效的页面
    if (len(getProductRowNodes(xml))  <= 0 ):
        clr.print_red_text("This page is not valid product page. URL ")

    try:
        nextPageNode = getNextProductPageNode(xml)
        # 获得productlist页面中的product行集节点对象
        nodes = getProductRowNodes(xml)

        if nodes:
            for node in nodes:
                # 解析一个行对象为一个Product对象
                result = parseSingleResultRow(node,2)
                if result:
                    threads.append(result)

        else:
            clr.print_red_text('Cant not parse Shop thread~')

    except Exception as err:
        clr.print_red_text(err+' parse Shop ProductPage Error')


    clr.print_green_text("End of parse Shop products ")

    return nextPageNode




def parseResultPage(xml,proIndex):
    ret = False
    jasonNode=getJsons(xml,1)
    global threads,clr
    resNode=jasonNode["mods"]["itemlist"]["data"]
    if(resNode == None or len(resNode) == 0):
        return ret

    nodes=resNode["auctions"]

    if(nodes == None  or len(nodes) == 0):
        return ret

    try:
        if  nodes:
            if proIndex:
                for  index,node in enumerate(nodes):
                    if(index<proIndex):
                        result = parseSingleResultRow(node,1)
                        if result:
                            threads.append(result)
                            ret=True

                    if( index>=proIndex):
                        ret=False
                        return ret


            else:
                for node in nodes:
                    result = parseSingleResultRow(node,1)
                    if result:
                        threads.append(result)
                        ret = True
                return ret
        else:
            clr.print_red_text('NO Result!')
    except Exception as err:
        clr.print_red_text(err)



def getProductRowNodes(html):

        items =[]
        html=html.replace('\\"','"')
        html=html.replace('"\\','"')
        index = html.find("<dl class=\"item")

        while(index > -1):
            html = html[index:]
            pos = html.find("</dl>")
            if(pos > -1):
                item = html[0:pos+5]
                html = html[pos+5:]
                items.append(item)
            else:
                break
            index = html.find("<dl class=\"item")
        return items

def isTopProduct(theTopnum):
        if (theTopnum == 0):
            return True
        return False

def getTopPage(theTopNum):
    if(theTopNum<=44):
        return 1
    thePgNum=str(theTopNum/44)
    if(thePgNum.find('.')<0):
        return thePgNum
    thePgNum=int(thePgNum[0:thePgNum.find('.')])
    if(theTopNum>thePgNum*44):
        thePgNum=thePgNum+1
    return thePgNum

def getTopPro(theTopNum):
    pgNum=getTopPage(theTopNum)
    topProNum=0
    if(theTopNum==44*pgNum):
        topProNum=0
        return topProNum

    if(theTopNum<44*pgNum):
        topProNum=theTopNum-((pgNum-1)*44)
        return topProNum
    return topProNum


def isMatchResult(jsons):
    nodes = jsons
    if  nodes["mods"]["tips"]:
        if  rNode["data"]:
            return False

    noNode=aNode.html

    if noNode:
        if noNode.find('搜索结果较少'):
            return False
        return True
    return False

def parseSalesVolume(value):

    if(value.find('万')>0):
        value = value.replace('万','')
        value=value*10000

    return value.replace('人收货','')


def parseNumOfReview(value):

    if(value.find('万')>0):
        value = value.replace('万','')
        value = value*10000

    return value

def parseSubject(string):
	index=string.find('item-name')
	if not index:
		print('Can Not parse subject!')
	string=string[index:]
	if string.find('">'):
		index=string.find('>')
	string=string[index+1:]
	if string.find('</a>'):
		index=string.find('</a>')
	string=string[0:index]
	string=string.replace('<span class=\"h\">','')
	string=string.replace('</span>','')
	return string

def parseUrl(string):
    index = string.find('item-name')
    if index <0:
        print("Can not parse URL")
    stringpa = string[index:]
    index  =stringpa.find('//detail')
    if index < 0:
        start = string.find('href="//detail')
        if start < 0 :
            print("cannot parse Url")
        end = string.find('"',start+14)
        if end < 0:
            print("cannot parse Url ")
        stringpa = string[start+6:end]
        index = stringpa.find('&amp')
        stringpa = stringpa[0:index]
    else:
        stringpa = stringpa[index:]
        index = stringpa.find('"')
        stringpa= stringpa[0:index]
        if stringpa == "" or stringpa is None:
            st = string.find('//detail')
            if st < 0:
                print("can not parse Url")
            end = string.find('&amp',st)
            stringpa = stringpa[index+8:end]

    return 'http:'+stringpa

def parsePrice(string):
	index=string.find('c-price')
	if(index<0):
		print("Can not parse Price.")
	string=string[index:]
	index=string.find('</span>')
	string=string[9:index]
	return string.replace(' ','')


def parseComments(string):
	index=string.find('评价:')
	if(index<0):
		return '推荐商品'
	
	string=string[index+3:]
	index=string.find('</span>')
	string=string[0:index]
	return string

def parseSum(string):
	index=string.find('sale-num">')
	if(index<0):
		return 0
	
	string=string[index:]
	index=string.find('</span>')
	string=string[10:index]
	return string

def parseProId(proUrl):
    proId = 0
    if not proUrl:
        return proId
    if proUrl.find('id=') > 0:
        proId=re.search('id=(\d+)',proUrl).group(1)
    return proId

def parseSingleResultRow(rowNode,parse_type):
    global clr, theSeller, theKeywordID, theUrl, theScrapecomment, theComment_type, theComment_filter, theSiteId,theKeyword,theTopnum
    try:
         if parse_type == 1:
                 title = rowNode["raw_title"]
                 url = "https:"+rowNode["detail_url"]
                 price = rowNode["view_price"]
                 marketPrice = rowNode["reserve_price"]
                 salesVolume = parseSalesVolume(rowNode["view_sales"])
                 numOfReview = parseNumOfReview(rowNode["comment_count"])
                 sellerName = rowNode["nick"]
                 category = None
                 keywordID = theKeywordID
                 promotions = None
                 reviewStar = 0
                 siteId = theSiteId
                 domain = 'detail.tmall.com' if (rowNode["detail_url"]).find('tmall')>-1 else 'detail.taobao.com'
                 productId = rowNode["nid"]
                 numOfFavorite = 0
                 sellerUrl = "https:"+ rowNode["shopLink"]
                 tags = None
                 scrapecomment = theScrapecomment
                 skuid = None
                 weight = 0
                 stock = 0
                 koubei = 0
                 type = None
                 lastScrapeDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                 comment_type = theComment_type
                 comment_filter = theComment_filter

                 thread = [title,url,price,marketPrice,salesVolume,numOfReview,sellerName,category,keywordID,promotions,reviewStar,siteId,domain,productId,numOfFavorite,sellerUrl,tags,scrapecomment,skuid,weight,stock,koubei,type,lastScrapeDate,comment_type,comment_filter]
                 return  thread

         elif  parse_type == 2 :

                title = parseSubject(rowNode)
                url =  parseUrl(rowNode)
                price = parsePrice(rowNode)
                marketPrice = None
                salesVolume = parseSum(rowNode)
                numOfReview = parseComments(rowNode)
                sellerName = theSeller
                category = None
                keywordID = theKeywordID
                promotions = None
                reviewStar = 0
                siteId = theSiteId
                domain = 'detail.tmall.com'
                productId = parseProId(url)
                numOfFavorite = 0
                sellerUrl = theUrl
                tags = None
                scrapecomment = theScrapecomment
                skuid = None
                weight = 0
                stock = 0
                koubei = 0
                type = None
                lastScrapeDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                comment_type = theComment_type
                comment_filter = theComment_filter

                thread = [title, url, price, marketPrice, salesVolume, numOfReview, sellerName, category, keywordID, promotions,reviewStar, siteId, domain, productId, numOfFavorite, sellerUrl, tags, scrapecomment, skuid, weight,stock, koubei, type, lastScrapeDate, comment_type, comment_filter]
                return thread


    except Exception as err:
        clr.print_red_text(err)



def doCapture(keyword, keywordID,topnum,scrapecomment,comment_type,comment_filter):
    global clr,theKeyword,theKeywordID,theScrapecomment,theTopnum,theComment_type,theComment_filter,theSiteId,threads
    theKeyword=keyword
    theKeywordID=keywordID
    theScrapecomment=scrapecomment
    theTopnum=int(topnum)
    theComment_type=int(comment_type)
    theComment_filter=comment_filter

    theSiteId=3000
    parse_type = 1

    try:
        pageNum = 0

        #check page
        threads = []
        hasNextPage = False

        if isTopProduct(theTopnum):
            while(True):
                pageNum += 1
                if(pageNum>100):
                    break

                clr.print_green_text('Starting parse page ' + str(pageNum))
                # sleepnum = random.uniform(2, 4)
                # clr.print_green_text("Wait for " + str(int(sleepnum)) + " Seconds!")
                # time.sleep(sleepnum)

                xml = loadProductList(theKeyword,pageNum)
                hasNextPage = parseResultPage(xml,None)
                if  not hasNextPage:
                    break
        if  not  isTopProduct(theTopnum):
                topNum = theTopnum
                topPage = getTopPage(topNum)
                topProNum = getTopPro(topNum)
                while(True):
                        pageNum += 1
                        if (pageNum > topPage):
                            break
                        if (pageNum > 100):
                            break
                        clr.print_green_text('  Start parsing page ' + str(pageNum))
                        if (topProNum == 0):
                                # sleepnum = random.uniform(2, 4)
                                # clr.print_green_text("  Wait for " + str(int(sleepnum)) + " Seconds!")
                                # time.sleep(sleepnum)
                                xml = loadProductList(theKeyword, pageNum)
                                hasNextPage=parseResultPage(xml,None)

                        if (topProNum > 0):
                                # sleepnum = random.uniform(2, 4)
                                # clr.print_green_text("  Wait for " + str(int(sleepnum)) + " Seconds!")
                                # time.sleep(sleepnum)
                                xml = loadProductList(theKeyword, pageNum)
                                if (pageNum == topPage):
                                            hasNextPage = parseResultPage(xml, topProNum)
                                else:
                                            hasNextPage = parseResultPage(xml,None)
                        if not hasNextPage:
                                break
    
        return threads

    except Exception as err:
        print(err)


def shop_doCapture(keywordID,keyword,topnum, url,scrapecomment,comment_type,comment_filter):
    
    global theKeywordID,theScrapecomment,theUrl,theComment_type,theComment_filter,theSiteId,theKeyword,clr,theSeller,theDomain,threads
    theKeywordID=keywordID
    theScrapecomment=scrapecomment
    theTopnum=int(topnum)
    theUrl = url
    theSiteId = 3002
    theComment_type=int(comment_type)
    theComment_filter=comment_filter
    theIdx=0
    parse_type = 2
    threads = []
    if url.find('.com') > 0:
        theDomain = url[0:url.find('.com') + 4]
    else:
        theDomain ='tmall.com'

    try:
        theKeyword=keyword
        if keyword == None or keyword == 'null' or keyword == '' :
            if url.find('search=y') < 0:
                url = theDomain+'/search.htm?orderType=hotsell_desc'
            
        else:
            url = theDomain+'/search.htm?q='+keyword+'&search=y&orderType=hotsell_desc&tsearch=y'
    
        xml = requests.get(url,timeout = 20).text
        xml = etree.HTML(xml)

        if  xml.xpath('.//a[@class ="shop-name"]/span') :
            theSeller = xml.xpath('.//a[@class ="shop-name"]/span')[0].xpath('string(.)').strip()    #商户名称
        else:
            theSeller = None

        hasNextPage = True
        while hasNextPage:
            if xml.xpath('.//input[@id= "J_ShopAsynSearchURL"]'):
                theSearchUrl = xml.xpath('.//input[@id = "J_ShopAsynSearchURL"]/@value')
                theSearchUrl = theSearchUrl[0].strip().replace('&amp;', '')
            else:
                break
            jsons =getJsons(theSearchUrl, parse_type)
            nextPageButton =parseProductPage(jsons)
            hasNextPage = True  if  nextPageButton and ( theIdx<=theTopnum or theTopnum==0) else False
            if hasNextPage:
                try:
                    xml = requests.get(nextPageButton,timeout = 20).text
                    xml = etree.HTML(xml)
                except Exception as err:
                    clr.print_red_text(err)
        return threads
    except Exception as err:
        clr.print_red_text(err)


def main():

    global clr
    clr = Color()
    clr.print_green_text('*'*40)
    clr.print_green_text('##  Python  3.4')
    clr.print_green_text('##  Author  Liam')
    clr.print_green_text('##  Date   11/16/2016')
    clr.print_green_text('##  Crawl   Tmall_Thread2.0(Keyword & Shop)')
    clr.print_green_text('*'*40)

    clr.print_green_text('Enter to Open File')
    dlg = win32ui.CreateFileDialog(1)   # 表示打开文件对话框
    dlg.SetOFNInitialDir('C:/')   # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()
    clr.print_green_text('Open File or directory: '+filename)
    # f = open(os.getcwd()+r'/indexCrawl.txt','rb')
    if filename is None or filename == '':
       sys.exit(0)
    f = open(filename,'rb')
    task_lines = [i for i in f.readlines()]
    f.close()

    count = 0
    allthread = []
    data =[]


    try:

        for line in task_lines:
            try:
                count += 1
                line = str(line, encoding='utf-8')
                line = line.replace(')','').replace('main(','').replace('\'','')
                line_split = line.strip()
                
                if not line:
                    continue
                line_split = line_split.split(',')
                clr.print_green_text('Start Parsing Keyword/Shop : '+str(line_split))
                if len(line_split) == 6 :
                    data = doCapture(line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5])
                    clr.print_green_text('KeyWord '+str(line_split)+ ' parsing Successfully!')
                elif len(line_split) == 7:
                    data = shop_doCapture(line_split[0],line_split[1],line_split[2],line_split[3],line_split[4],line_split[5],line_split[6])
                    clr.print_green_text(' Shop '+str(line_split)+ ' parsing Successfully!')
                for i in data:
                    allthread.append(i)
                clr.print_green_text ('Counts '+str(len(allthread))+' threads')
                if len(allthread) > 10000:    #避免消耗内存过大机器崩溃
                    getExcel(allthread)
                    allthread =[]
                waitTime = random.uniform(2, 4)
##                clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
                # time.sleep(waitTime)
            except Exception as err:
                clr.print_red_text (err)

        getExcel(allthread)

    except Exception as err:
        clr.print_red_text(err)


def getExcel(data):
    global clr
    try:
        title = ['title','url','price','marketPrice','salesVolume','numOfReview','sellerName','category','keywordID','promotions','reviewStar','siteId','domain','productId','numOfFavorite','sellerUrl','scrapecomment','skuid','weight','stock','koubei','type','lastScrapeDate','comment_type','comment_filter']
        file_name = '%s%s' % ('Output_',("%d" % (time.time() * 1000)))

        workbook = wx.Workbook(file_name+'.xls')
        worksheet = workbook.add_worksheet('Info')
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
