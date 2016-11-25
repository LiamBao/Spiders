# -*- coding: utf-8 -*-
import re, ctypes,requests,random,os,json,ctypes,win32ui,sys,math,time,datetime

from lxml import etree
import xlsxwriter as wx
from .colorFont import Color
import .dateParse
from .Autohome import AutohomeClient
from .config import postCrawlFlag,postData,postDateTime

__all__ = ['BBSParse']

class BBSSpider(object):
	"""docstring for autoHome101"""
	def __init__(self, url):
		# super(autoHome101, self).__init__()
		# http://club.autohome.com.cn/bbs/forum-c-2896-1.html'?type=101'
		self.__url          = ''
        self.__baseClient   = None
        self.__client       = None
        self.__functionDict = {'default': lambda x: 0}
        if 'http://' == url[:7] or 'https://' == url[:8]:
            self.__url = url
        else:
            self.__url = 'http://' + url


        for u, bc in {'club.autohome.com'   : AutohomeClient,
                'cehome.com'			    : DouYuDanMuClient, 
                ''}.items() :
            if re.match(r'^(?:http://)?.*?%s/(.+?)$' % u, url):
                self.__baseClient = bc; break

        return fn
    def start(self, blockThread = False, pauseTime = .1):
        if not self.__baseClient: return False
        self.__client = self.__baseClient(self.__url)
        receiveThread = threading.Thread(target=self.__client.start)
        receiveThread.setDaemon(True)
        receiveThread.start()
        def _start():
            while self.__isRunning:
                if self.__client.msgPipe:
                    msg = self.__client.msgPipe.pop()
                    fn = self.__functionDict.get(msg['MsgType'],
                        self.__functionDict['default'])
                    try:
                        fn(msg)
                    except:
                        traceback.print_exc()
                else:
                    time.sleep(pauseTime)
        if blockThread:
            try:
                _start()
            except KeyboardInterrupt:
                print('Bye~')
        else:
            danmuThread = threading.Thread(target = _start)
            danmuThread.setDaemon(True)
            danmuThread.start()
        return True
    def stop(self):
        self.__isRunning = False
        if self.__client: self.__client.deprecated = True