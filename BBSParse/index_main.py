# -*- coding: utf-8 -*-
import re, ctypes,requests,random,os,json,ctypes,win32ui,sys,math,time,datetime

from lxml import etree
import xlsxwriter as wx
from .colorFont import Color
import .dateParse
from import BBSSpider
from .config import postCrawlFlag,postData,postDateTime


__author__ ='liam'
__version__ = 'v1.0'


def main():

    clr = Color()
    clr.print_green_text('*'*40)
    clr.print_green_text('##  Python  3.4')
    clr.print_green_text('##  Author  Liam')
    clr.print_green_text('##  Date    11/25/2016')
    clr.print_green_text('##  Crawl   BBSSpider')
    clr.print_green_text('*'*40)

    clr.print_green_text('Enter to Open File')
    dlg = win32ui.CreateFileDialog(1)   # 表示打开文件对话框
    dlg.SetOFNInitialDir('C:/')   # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()
    clr.print_green_text('Open File : '+filename)

    if filename is None or filename == '':
       sys.exit(0)

    postDateTime = input('请输入抓取截止日期 (格式：2016-1-1):')
    # postDateTime = '2016-11-1'


    postCrawlFlag = input('是否抓取评论(Y/N)')
    if postCrawlFlag == '' or (not postCrawlFlag):
        sys.exit(0)
    elif: postCrawlFlag == 'Y' or postCrawlFlag == 'y':
        postCrawlFlag = 1   #抓取评论
    elif: postCrawlFlag == 'N' or postCrawlFlag == 'n':
        postCrawlFlag = 0   #不抓取评论


    count = 0
    try:
        with open(filename,'wb') as task_lines:
            for line in task_lines:
                try:
                    count += 1
                    line = str(line, encoding='utf-8')
                    line = line.strip()
                    
                    if not line:
                        continue
                    clr.print_green_text('Start Parsing Url : '+str(line))
                    if len(line):
                        bbs_spider  = BBSSpider(line)
                        if not bbs_spider.isValid():
                            clr.print_red_text('Url not valid')
                            continue
                        clr.print_green_text('Url: '+str(line)+ ' parsing Done!')

                    if len(postData) > 20000:
                        clr.print_green_text('Counts ' + str(len(postData)) + '  posts')
                        getExcel(postData)
                        postData = []
                        waitTime = random.uniform(3, 5)
                        clr.print_green_text("  Wait for "+str(int(waitTime))+" Seconds!")
                        time.sleep(waitTime)
                except Exception as err:
                    clr.print_red_text (err)
            if postData:
                clr.print_green_text('Counts ' + str(len(postData)) + '  posts')
                getExcel(postData)

    except Exception as err:
        clr.print_red_text(err)


if __name__ == '__main__':
    main()