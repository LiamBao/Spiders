# -*- coding: utf-8 -*-
##__author__ =='liam'
# python3.52
import re,time,random
import requests,json
import tkinter as tk
from tkinter import filedialog
import xlsxwriter as wx
from lxml import etree

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

def huajiao_get_live_status(url):

    xml = requests.get(url,headers = Headers,timeout = 10)
    xml = xml.content.decode('utf-8', 'replace').encode('utf8', 'replace')
    roomId = (re.search('com/user/(\d+)',url).group(1),0)[re.search('com/user/(\d+)',url) == None]
    xml = etree.HTML(xml)
    fansNum = xml.xpath('.//ul[@class="clearfix"]/li/p')[1].xpath('string(.)').strip()
    jsonUrl = "http://webh.huajiao.com/User/getUserFeeds?fmt=jsonp&uid="+str(roomId)+"&_callback=jQuery&_="
    jsonXml = requests.get(jsonUrl,headers = Headers,timeout = 10).text
    jsonXml = jsonXml.replace('/**/jQuery(','').replace('});','}')
    jsonXml = json.loads(jsonXml)
    if jsonXml["errno"] == 0:
        videoXML =  jsonXml["data"]["feeds"]
        for video in videoXML:
            get_Each_video(video,fansNum,roomId,url)
        
def get_Each_video(xml,fansNum,roomId,url):
    global LiveData
    userName = xml["author"]["nickname"]
    onlineNum = xml["feed"]["watches"]
    cateName = str(xml["feed"]["tags"])
    roomName = xml["feed"]["title"]
    videoDate = xml["feed"]["publishtime"]
    numOfReplies = xml["feed"]["replies"]
    numOfPraises = xml["feed"]["praises"]

    info = [videoDate,roomId,userName,onlineNum,cateName,fansNum,numOfPraises,numOfReplies,roomName,url]
    LiveData.append(info)

def getExcel(data):
    try:
        print(data)

        title = ['DateTime', 'roomId', 'userName', 'onlineNum','cateName', 'fansNum', 'numOfPraises','numOfReplies', 'roomName','url']
        file_name = 'Output_Huajiao'+ str((time.time() * 1000))[8:]

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


def main():
    print('*' * 40)
    print('##  Python  3.52')
    print('##  Author  Liam')
    print('##  Date    02/28/2017')
    print('##  Huajiao Online Data')
    print('*' * 40)

    print('\r\n请选择账户信息文件')
    dialog = tk.Tk()
    dialog.withdraw()
    filename = filedialog.askopenfilename()
    if filename is None or filename == '':
        sys.exit(0)
    # filename = './test.txt'
    print(filename)
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
                if not line and re.search('.*?huajiao.*?',line):
                    continue

                huajiao_get_live_status(line)
                waitTime = random.uniform(2, 4)
                time.sleep(waitTime)
            except Exception as err:
                print(err)
        getExcel(LiveData)
    except Exception as err:
        print(err)
    finally:
        print("Done")

if __name__ == '__main__':
    main()