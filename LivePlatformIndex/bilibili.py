# -*- coding: utf-8 -*-
##__author__ =='liam'
# python3.52
import re,time,random
import requests
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


def getExcel(data):
    try:
        title = ['userlink','userId','userName', 'total_number_of_plays', 'num_of_fans', 'num_of_follwed', 'num_of_play','num_of_review', 'video_review','favorites','num_of_share','url']
        file_name = 'Output_Douyu'+ str((time.time() * 1000))[10:]
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


def bilibili_get_info(url):
	global LiveData

	userId = (re.search('bilibili.com/(\d+)',url).group(1),0)[re.search('bilibili.com/(\d+)',url)== None]
	if not userId:
		logger.error(url+" invalidUrl")
	[userName,total_number_of_plays,num_of_fans,num_of_follwed] = get_main_Info(url,userId)

	videoListUrl = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid='+str(userId)+'&page=1&pagesize=20'
	jsonXml = requests.get(videoListUrl,timeout =10)
	if jsonXml and jsonXml.json()["status"]:
		jsonXml = jsonXml.json()
		Videolist = jsonXml["data"]["vlist"]
		for video in Videolist:
			info = get_each_video(video)
			LiveData.append([userlink,userId,userName,total_number_of_plays,num_of_fans,num_of_follwed]+info)
	else:
		logger.error(url+": NO result")


def get_main_Info(url,userId):

	Headers = {
	    "Accept-Encoding": "gzip, deflate, br",
	    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
	    "Connection": "keep-alive",
	    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	    "User-Agent": random.choice(USER_AGENTS),
	    "Referer": "http://space.bilibili.com/"+str(userId),
	    "Content-Type":"application/x-www-form-urlencoded"
	}
	getInfo_url = "http://space.bilibili.com/ajax/member/GetInfo"
	form_data = {
		"mid":userId,
		"_": str(time.time()*1000000)
	}
	print(form_data)
	res = requests.post(getInfo_url,headers = Headers,data = form_data, timeout =10)
	if res.json() and res.json()["status"]:
		res = res.json()
		userName= res["data"]["name"]
		total_number_of_plays= res["data"]["playNum"]
		num_of_fans=res["data"]["fans"]
		num_of_follwed=res["data"]["friend"]
		return [userName,total_number_of_plays,num_of_fans,num_of_follwed]
	else:
		return None	


def get_each_video(xml):
	num_of_play = xml["play"]
	num_of_review = xml["review"]
	video_review = xml["video_review"]
	favorites = xml["favorites"]
	url = "http://api.bilibili.com/archive_stat/stat?aid="+str(xml["aid"])
	res = requests.get(url,timeout=10)
	if res.status_code == 200:
		num_of_share = res.json()["data"]["share"]
	else:
		num_of_share = 0
	info = [num_of_play, num_of_review, video_review, favorites,num_of_share,url]
	return info

def main():
    print('*' * 40)
    print('##  Python  3.52')
    print('##  Author  Liam')
    print('##  Date    03/28/2017')
    print('##  BilibiliIndex Data')
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
                if not line and re.search('.*?bilibili.*?',line):
                	print(line+": Invalid Url")
                	continue
                bilibili_get_info(line)
                waitTime = random.uniform(2, 4)
                time.sleep(waitTime)
            except Exception as err:
                print(err)
        print(LiveData)
        getExcel(LiveData)
    except Exception as err:
        print(err)
    finally:
        print("Done")

if __name__ == '__main__':
    main()

