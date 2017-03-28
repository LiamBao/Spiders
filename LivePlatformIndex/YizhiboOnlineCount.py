# -*- coding: utf-8 -*-
##__author__ =='liam'
# python3.52
import re,time,random
import requests
import tkinter as tk
from tkinter import filedialog
import xlsxwriter as wx
from lxml import etree
import datetime

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

Headers = {
    # "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": random.choice(USER_AGENTS)
}


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

def getExcel(data):
    try:
        print(data)
        title = ['DateTime', 'roomId', 'userName', 'onlineNum', 'fansNum',"followNum",'cateName', 'roomName','url','numofLikes','numofComment']
        file_name = 'Output_Yizhibo'+ str((time.time() * 1000))[8:]

        workbook = wx.Workbook(file_name + '.xlsx')
        worksheet = workbook.add_worksheet('info')
        for i in range(len(data)):
            for j in range(len(title)):
                if i == 0:
                    worksheet.write(i, j, title[j])
                worksheet.write(i + 1, j, data[i][j])
        workbook.close()
        print('\n File ' + file_name + ' Done!')
    except Exception as err:
        print(err)

def parseDateStr(date_pa):
    return time.strftime("%Y-%m-%d %H:%M:%S", date_pa)

def parseDateStrToStamp(datestr):
       return time.mktime(time.strptime(datestr,'%Y-%m-%d %H:%M:%S'))


def yizhibo_get_live_status(url):
    # http: // www.yizhibo.com / member / personel / user_info?memberid = 55256502
    infoUrl = 'http://www.yizhibo.com/member/personel/user_works?memberid='
    userID = re.search('memberid=(\d+)',url).group(1)
    infoUrl += str(userID)
    print(url)

    urlPage = requests.get(url, headers = Headers, timeout=20)
    if urlPage:
        urlPage = urlPage.text
        if(re.search('粉丝 <span>(\d+)</span>',urlPage)):
            fansNum = re.search('粉丝 <span>(\d+)</span>',urlPage).group(1)
        else:
            fansNum = 0

        if(re.search('关注 <span>(\d+)</span>',urlPage)):
            followNum = re.search('关注 <span>(\d+)</span>',urlPage).group(1)
        else:
            followNum = 0
    try:
        page = requests.get(infoUrl, headers = Headers, timeout = 20)
        page = page.content.decode('utf-8', 'replace').encode('utf8', 'replace')
        if page:
            xml = etree.HTML(page)
            # firstVideo：
            xml = xml.xpath('.//ul[@class = "index_all index_all_all cf"]//li[@class="index_all_common index_hf"]')
            if xml and len(xml)>0:
                for video in xml:
                    get_Each_videoInfo(url,userID,fansNum,followNum,video)
                
    except Exception as err:
        print(err)

def get_Each_videoInfo(url,userID,fansNum,followNum,xml):
    try:
        global LiveData
        roomId = userID
        videoDate =(xml.xpath('.//div[@class="index_time fr"]')[0].xpath('string(.)').strip(), '')[len(xml.xpath('.//div[@class="index_time fr"]')) == 0]
        if videoDate:
            if re.search('(\d+)-(\d+)-(\d+)', videoDate):
                videoDate = re.search('(\d+-\d+-\d+)', videoDate).group(1)
                videoDate = parseDateStr(parseDate(videoDate))
            else:
                videoDate= (parseDate(str(videoDate).replace('发起了一个直播',''))).strftime('%Y-%m-%d %H:%M:%S')
                print(videoDate)
        userName = (xml.xpath('.//div[@class="index_name fl txt-cut"]')[0].xpath('string(.)').strip(), '')[len(xml.xpath('.//div[@class="index_name fl txt-cut"]')) == 0]
        onlineNum = (xml.xpath('.//div[@class="index_num fl"]')[0].xpath('string(.)').strip(), 0)[len(xml.xpath('.//div[@class="index_num fl"]')) == 0]
        cateName = ''
        numofLikes = (xml.xpath('.//div[@class="index_zan"]')[0].xpath('string(.)').strip(), 0)[len(xml.xpath('.//div[@class="index_zan"]')) == 0]
        numofComment = (xml.xpath('.//div[@class="index_msg"]')[0].xpath('string(.)').strip(), 0)[len(xml.xpath('.//div[@class="index_msg"]')) == 0]
        roomName = userName
        Info =[videoDate, roomId, userName, onlineNum, fansNum,followNum,cateName, roomName,url,numofLikes,numofComment]
        if Info:
            LiveData.append(Info)

    except Exception as err:
        print(err)


def main():
    print('*' * 40)
    print('##  Python  3.52')
    print('##  Author  Liam')
    print('##  Date    02/28/2017')
    print('##  Yizhibo Online Index')
    print('*' * 40)

    print('\r\n请选择账户信息文件')
    dialog = tk.Tk()
    dialog.withdraw()
    filename = filedialog.askopenfilename()
    if filename is None or filename == '':
        sys.exit(0)
    # filename = './test.txt'
    print("filename "+filename)
    f = open(filename, 'rb')
    task_lines = [i for i in f.readlines()]
    f.close()

    global LiveData
    LiveData = []
    count = 0
    try:
        for line in task_lines:
            try:
                count += 1
                line = str(line, encoding='utf-8')
                line = line.strip()
                if not line or not re.search('.*?yizhibo.*?',line):
                    continue
                if re.search('//yizhibo',line):
                    line=line.replace("//yizhibo","//www.yizhibo")
                infoData = yizhibo_get_live_status(line)
                # waitTime = random.uniform(2, 4)
                # time.sleep(waitTime)
            except Exception as err:
                print(err)
        getExcel(LiveData)
        print(LiveData)
    except Exception as err:
        print(err)
    finally:
        print("Done")

if __name__ == '__main__':
    main()