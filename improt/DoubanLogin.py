#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import json
import os
import re
import sys
##import subprocess
##from bs4 import BeautifulSoup as BS


class DoubanClient(object):

    """连接知乎的工具类，维护一个Session
    2015.11.11

    用法：

    client = ZhiHuClient()

    # 第一次使用时需要调用此方法登录一次，生成cookie文件
    # 以后可以跳过这一步
    client.login("username", "password")   

    # 用这个session进行其他网络操作，详见requests库
    session = client.getSession()
    """

    loginURL = r"https://www.douban.com/login"
    homeURL = r"http://www.douban.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Host": "www.douban.com",
        "Connection":"keep-alive",
        "Cache-Control":"max-age=0",
        # "Referer":"https://www.baidu.com/link?url=BCG5AfxNkL6vibSGQS5bypnPCS1cASjrzeiUkBCODrG&wd=&eqid=e2bd91340002c19400000004582a86f3",
        "Upgrade-Insecure-Requests": "1"
    }

    captchaFile = os.path.join(sys.path[0], "captcha.gif")
    cookieFile = os.path.join(sys.path[0], "cookie")

    def __init__(self):
        os.chdir(sys.path[0])  # 设置脚本所在目录为当前工作目录

        self.__session = requests.Session()
        self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
        # 若已经有 cookie 则直接登录
        self.__cookie = self.__loadCookie()
##        if self.__cookie:
##            print("检测到cookie文件，直接使用cookie登录")
##            self.__session.cookies.update(self.__cookie)
##            soup = BS(self.open(r"http://www.douban.com/").text, "html.parser")
##            print("已登陆账号： %s" % soup.find("span", class_="name").getText())
##        else:
##            print("没有找到cookie文件，请调用login方法登录一次！")

    # 登录
    def login(self, username, password):
        """
        验证码错误返回：
        {'errcode': 1991829, 'r': 1, 'data': {'captcha': '请提交正确的验证码 :('}, 'msg': '请提交正确的验证码 :('}
        登录成功返回：
        {'r': 0, 'msg': '登陆成功'}
        """
        self.__username = username
        self.__password = password
        self.__loginURL = self.loginURL
        # 随便开个网页，获取登陆所需的_xsrf
##        html = self.open(self.homeURL).text
##        soup = BS(html, "html.parser") 
        # _xsrf = soup.find("input", {"name": "_xsrf"})["value"]

        # 下载验证码图片
        while True:

            # 发送POST请求
            data = {
                "source": None,
                "form_password": self.__password,
                "form_email":self.__username,
                "login": "登录"
            }
            print(self.__loginURL)
            res = self.__session.post(self.__loginURL, data=data)
            print("=" * 50)
            print(res.text) # 输出脚本信息，调试用
            if res.json()["r"] == 0:
                print("登录成功")
                break
            else:
                print("登录失败")
                print("错误信息 --->", res.json()["msg"])

    def __saveCookie(self):
        """cookies 序列化到文件
        即把dict对象转化成字符串保存
        """
        with open(self.cookieFile, "w") as output:
            cookies = self.__session.cookies.get_dict()
            json.dump(cookies, output)
            print("=" * 50)
            print("已在同目录下生成cookie文件：", self.cookieFile)

    def __loadCookie(self):
        """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
        if os.path.exists(self.cookieFile):
            print("=" * 50)
            with open(self.cookieFile, "r") as f:
                cookie = json.load(f)
                return cookie
        return None

    def open(self, url, delay=0, timeout=10):
        """打开网页，返回Response对象"""
        if delay:
            time.sleep(delay)
        return self.__session.get(url, timeout=timeout)

    def getSession(self):
        return self.__session

if __name__ == '__main__':
    client = DoubanClient()

    # 第一次使用时需要调用此方法登录一次，生成cookie文件
    # 以后可以跳过这一步
    client.login("liam.bao@cicdata.com", "cicdata123456")

    # 用这个session进行其他网络操作，详见requests库
    session = client.getSession()
