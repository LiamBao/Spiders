# -*- coding: utf-8 -*-
import re, ctypes,requests,random,os,json,ctypes,win32ui,sys,math,time,datetime

from lxml import etree
import xlsxwriter as wx
from .colorFont import Color
import .dateParse

from .Autohome import AutohomeClient


__author__ ='liam'
__version__ = 'v1.0'


class autoHome101(object):
	"""docstring for autoHome101"""
	def __init__(self, url):
		# super(autoHome101, self).__init__()
		# http://club.autohome.com.cn/bbs/forum-c-2896-1.html'?type=101'
		self.__url          = ''
        self.__baseClient   = None
        self.__client       = None
        self.__functionDict = {'default': lambda x: 0}
        self.__isRunning    = False

		if 'http://club.autohome.com.cn' == url[:32] and url.find('?type=101')>-1:
			self.__url = url
		else:
			input('Url Error! Enter to exit')
			exit()

        for u, bc in {'club.autohome.com'   : AutohomeClient,
                'cehome.com'			    : DouYuDanMuClient, 
                ''}.items() :
            if re.match(r'^(?:http://)?.*?%s/(.+?)$' % u, url):
                self.__baseClient = bc; break
    def __register(self, fn, msgType):
        if fn is None:
            if msgType == 'default':
                self.__functionDict['default'] = lambda x: 0
            elif self.__functionDict.get(msgType):
                del self.__functionDict[msgType]
        else:
            self.__functionDict[msgType] = fn
    def isValid(self):
        return self.__baseClient is not None
    def default(self, fn):
        self.__register(fn, 'default')
        return fn
    def danmu(self, fn):
        self.__register(fn, 'danmu')
        return fn
    def gift(self, fn):
        self.__register(fn, 'gift')
        return fn
    def other(self, fn):
        self.__register(fn, 'other')
        return fn
    def start(self, blockThread = False, pauseTime = .1):
        if not self.__baseClient or self.__isRunning: return False
        self.__client = self.__baseClient(self.__url)
        self.__isRunning = True
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