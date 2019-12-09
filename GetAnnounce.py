import Logger
import requests, json
from lxml import etree
import datetime, operator, functools
from urllib import parse


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
    __max = 2

    l = Logger.Logger()

    def __testHttp(self, target):
        try:
            self.l.info("正在测试网络连通...")
            return requests.get(target)
        except:
            return False

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)
        return cls.__obj

    def __init__(self, text):
        if self.__initFlag is False:
            if text == "" or text == " ":
                self.__domain = "https://oa.jlu.edu.cn/"
            else:
                self.__domain = text
            if self.__testHttp(self.__domain):
                self.l.notice("Http连接成功！")
                self.l.info("目标地址：" + self.__domain)

            else:
                self.l.error("连接错误！请检查网络连接！")
                raise Exception("NetworkError")
        self.__initFlag = True

    def __cmpDatetime(o, a, b):
        aDatetime = datetime.datetime.strptime(a['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')
        bDatetime = datetime.datetime.strptime(b['time'], '%Y年%m月%d日 %H:%M\xa0\xa0')
        if aDatetime > bDatetime:
            return -1
        elif aDatetime < bDatetime:
            return 1
        else:
            return 0

    def createCache(self):
        self.__cacheList = []
        self.__cacheContent = []
        self.l.info("正在获取网页内容...")
        html = requests.get(self.__domain + self.__direct + self.__list).text
        self.l.notice("获取成功！")
        data = etree.HTML(html)
        for i in range(1, self.__max):
            time = data.xpath('//*[@id="itemContainer"]/div[%d]/span/text()' % i)
            href = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/@href' % i)
            author = data.xpath('//*[@id="itemContainer"]/div[%d]/a[2]/text()' % i)
            title = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/text()' % i)
            self.l.info("获取到《%s》通知，发布时间%s" % (title[0], time[0]))
            self.__cacheList.append(
                {"title": title[0], "time": time[0], "href": self.__domain + self.__direct + href[0],
                 "author": author[0]})

        for i in self.__cacheList:
            tmpResult = ""
            tmpAttach = {}
            self.l.info("正在获取《%s》..." % i['title'])
            '''同时获取完整标题、时间'''
            html = requests.get(i['href'], headers=self.__header).text
            data = etree.HTML(html)
            content = data.xpath('/html/body//div')
            for j in content:
                if str(j.get('class')).find("content_time") != -1:
                    i['time'] = j.xpath('./text()')[0]
                    self.l.notice("完整时间：%s" % i['time'])
                    self.l.notice("链接：%s" % i['href'])
                elif str(j.get('class')).find("content_t") != -1:
                    i['title'] = j.xpath('./text()')[0]
                    self.l.notice("获取成功！完整标题：%s" % i['title'])
                if str(j.get('class')).find("content_font") != -1:
                    for k in j.xpath('.//p'):
                        for m in k.xpath('.//span'):
                            for x in m.xpath('./text()'):
                                tmpResult = tmpResult + x
                        tmpResult = tmpResult + "\t\n"
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

            self.__cacheContent.append(
                {'title': i['title'], 'address': i['href'], 'time': i['time'], 'author': i['author'],
                 'content': tmpResult, 'attach': tmpAttach})
            # 对时间进行排序
        self.__cacheContent.sort(key=functools.cmp_to_key(self.__cmpDatetime))

    def freshCache(self):
        # 首先需要复制原有缓存
        oldCache = self.__cacheContent.copy()
        # 重新创建缓存
        self.createCache()
        # 批量比较不同，将不同的内容放入缓存前方
        # 首先进行快比较
        if operator.eq(self.__cacheContent, oldCache):
            self.l.notice("缓存未更改！")
            return None
        else:
            k = 0
            newCache = []
            for i in self.__cacheContent:
                for j in oldCache:
                    if i['title'] != j['title']:
                        newCache.append(i)
                        k += 1
            for i in range(1, k):
                self.l.info("第%d条已删除。" % i)
                self.__cacheContent.pop()
            # return newCache
            self.__cacheContent.append(newCache)
            return newCache

    def get(self):
        return self.__cacheContent
