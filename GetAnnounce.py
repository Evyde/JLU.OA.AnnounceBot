import datetime
import functools
import requests
from urllib import parse

from lxml import etree


class GetAnnounce(object):
    __domain = ""
    __direct = "defaultroot/"
    __list = "PortalInformation!jldxList.action?channelId=179577"
    __cacheList = []
    __cacheContent = []
    __linkBaseUrl = "rd/download/BASEEncoderAjax.jsp"
    __downloadBaseUrl = "rd/download/attachdownload.jsp?res="
    __header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    __obj = None
    __initFlag = False
    __max = 31
    __logger = None
    __config = None

    def __cmpDatetime(self, a, b):
        aDatetime = datetime.datetime.strptime(a['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')
        bDatetime = datetime.datetime.strptime(b['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')

        # 比较进行到这里说明a, b都是置顶或非置顶，则按时间进行排序
        if aDatetime > bDatetime:
            return -1
        elif aDatetime < bDatetime:
            return 1
        else:
            return 0

    def __cmpIsTop(self, a, b):
        isATop = a['top']
        isBTop = b['top']
        if isATop == "[置顶]" and isBTop == "":
            return -1
        elif isATop == "" and isBTop == "[置顶]":
            return 1
        else:
            return 0

    def __sort(self, sortTarget):
        # 按时间排序
        self.__sortByTime(sortTarget)
        # 按是否置顶排序
        sortTarget.sort(key=functools.cmp_to_key(self.__cmpIsTop))
        return sortTarget

    def __sortByTime(self, sortTarget):
        sortTarget.sort(key=functools.cmp_to_key(self.__cmpDatetime))
        return sortTarget

    def __testHttp(self, target):
        try:
            self.__logger.info("正在测试网络连通...")
            return requests.get(target)
        except:
            return False

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)
        return cls.__obj

    def __init__(self, text, logger, cfg):
        self.__logger = logger
        self.__config = cfg
        if self.__initFlag is False:
            if text == "" or text == " ":
                self.__domain = "https://oa.jlu.edu.cn/"
            else:
                self.__domain = text
            if self.__testHttp(self.__domain):
                self.__logger.notice("Http连接成功！")
                self.__logger.info("目标地址：" + self.__domain)

            else:
                self.__logger.error("连接错误！请检查网络连接！")
                raise Exception("NetworkError")
        self.__initFlag = True

    def getList(self):
        self.__cacheList = []
        self.__cacheContent = []
        self.__logger.info("正在获取主页内容...")
        html = requests.get(self.__domain + self.__direct + self.__list).text
        self.__logger.notice("获取成功！")
        data = etree.HTML(html)
        for i in range(1, self.__max):
            time = data.xpath('//*[@id="itemContainer"]/div[%d]/span/text()' % i)
            href = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/@href' % i)
            author = data.xpath('//*[@id="itemContainer"]/div[%d]/a[2]/text()' % i)
            title = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/text()' % i)
            if data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/font/text()' % i):
                isTop = "[置顶]"
            else:
                isTop = ""
            self.__logger.info("获取到%s 《%s》通知，发布时间%s" % (isTop, title[0], time[0]))
            self.__cacheList.append(
                {"title": title[0], "time": time[0], "href": self.__domain + self.__direct + href[0],
                 "author": author[0], 'top': isTop})

        return self.__cacheList

    def getContents(self, target):
        rtnContent = []
        for i in target:
            tmpResult = ""
            tmpAttach = {}
            tmpLongTitle = ""
            self.__logger.info("正在获取%s《%s》..." % (i['top'], i['title']))
            '''同时获取完整标题、时间'''
            html = requests.get(i['href'], headers=self.__header).text
            data = etree.HTML(html)
            content = data.xpath('/html/body//div')
            for j in content:
                if str(j.get('class')).find("content_time") != -1:
                    time = j.xpath('./text()')[0]
                    timeStamp = int(datetime.datetime.strptime(time, "%Y年%m月%d日 %H:%M\xa0\xa0").timestamp())
                    self.__logger.info("完整时间：%s" % time)
                    self.__logger.info("链接：%s" % i['href'])
                elif str(j.get('class')).find("content_t") != -1:
                    tmpLongTitle = j.xpath('./text()')[0]
                    self.__logger.notice("获取成功！完整标题：%s" % tmpLongTitle)
                if str(j.get('class')).find("content_font") != -1:
                    """目前发现通知网页有两种方法，一种是经过混淆的，另一种是没有混淆的，先尝试有混淆的"""
                    for k in j.xpath('.//p'):
                        for m in k.xpath('.//text()'):
                            tmpResult = tmpResult + m
                        tmpResult = tmpResult + "\t\n"
                    tmpResult = tmpResult.replace("\xa0", " ")
                    if tmpResult == "":
                        tmpResultList = j.xpath('.//text()')
                        for l in tmpResultList:
                            tmpResult += str(l)
                        tmpResult = tmpResult.replace("\xa0", " ")
                        tmpResult = tmpResult.replace("    ", "\t\n\t")
                if str(j.get('class')).find("news_aboutFile") != -1:
                    # 附件存在
                    # 获取InfomationID
                    sc = str(html)
                    start = sc.find("informationId=")
                    start = sc.find("\'", start)
                    end = sc.find("\'", start + 1)
                    sc = sc[start + 1:end]
                    url = self.__domain + self.__direct + self.__linkBaseUrl
                    for k in j.xpath('.//span'):
                        attSave = str(k.get('id'))
                        attName = str(k.get('title'))
                        send = parse.quote(attSave + "@" + attName + "@" + str(sc))
                        send = "res=" + send
                        rJson = str(requests.post(url, send, headers=self.__header).text)
                        link = self.__domain + self.__direct + self.__downloadBaseUrl + str(rJson)
                        link = link.replace('\r', "")
                        link = link.replace('\n', "")
                        tmpAttach.update({str(k.get('title')): link})
            if timeStamp <= int(self.__config.get("common", "timeStamp")):
                if not rtnContent:
                    self.__logger.notice("无更新！")
                    break

                rtnContent = self.__sortByTime(rtnContent)
                print(rtnContent)
                self.__config.set("common", "timeStamp", str(rtnContent[0]['timeStamp']))
                rtnContent = self.__sort(rtnContent)
                break
            rtnContent.append(
                {'title': tmpLongTitle, 'address': i['href'], 'time': time, 'author': i['author'],
                 'content': tmpResult, 'attach': tmpAttach, 'sTitle': i['title'], 'top': i['top'],
                 'timeStamp': timeStamp})
        return rtnContent

    def get(self):
        return self.getContents(self.getList())
