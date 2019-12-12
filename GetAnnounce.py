from lxml import etree
import datetime, operator, functools, requests, Logger
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
    __max = 31

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
        isATop = a['top']
        isBTop = b['top']
        if isATop == "[置顶]" and isBTop == "":
            return 1
        elif isATop == "" and isBTop == "[置顶]":
            return -1
        # 比较进行到这里说明a, b都是置顶或非置顶，则按时间进行排序
        if aDatetime > bDatetime:
            return -1
        elif aDatetime < bDatetime:
            return 1
        else:
            return 0

    def createListCache(self):
        self.__cacheList = []
        self.__cacheContent = []
        self.l.info("正在获取主页内容...")
        html = requests.get(self.__domain + self.__direct + self.__list).text
        self.l.notice("获取成功！")
        data = etree.HTML(html)
        for i in range(1, self.__max):
            time = data.xpath('//*[@id="itemContainer"]/div[%d]/span/text()' % i)
            href = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/@href' % i)
            author = data.xpath('//*[@id="itemContainer"]/div[%d]/a[2]/text()' % i)
            title = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/text()' % i)
            if data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/font/text()' % i) != []:
                isTop = "[置顶]"
            else: isTop = ""
            self.l.info("获取到%s 《%s》通知，发布时间%s" % (isTop, title[0], time[0]))
            self.__cacheList.append(
                {"title": title[0], "time": time[0], "href": self.__domain + self.__direct + href[0],
                 "author": author[0], 'top': isTop})

        return self.__cacheList

    def createContentCache(self):
        for i in self.__cacheList:
            tmpResult = ""
            tmpAttach = {}
            tmpLongTitle = ""
            self.l.info("正在获取《%s》..." % i['title'])
            '''同时获取完整标题、时间'''
            html = requests.get(i['href'], headers=self.__header).text
            data = etree.HTML(html)
            content = data.xpath('/html/body//div')
            for j in content:
                if str(j.get('class')).find("content_time") != -1:
                    i['time'] = j.xpath('./text()')[0]
                    self.l.info("完整时间：%s" % i['time'])
                    self.l.info("链接：%s" % i['href'])
                elif str(j.get('class')).find("content_t") != -1:
                    tmpLongTitle = j.xpath('./text()')[0]
                    self.l.notice("获取成功！完整标题：%s" % tmpLongTitle)
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
                {'title': tmpLongTitle, 'address': i['href'], 'time': i['time'], 'author': i['author'],
                 'content': tmpResult, 'attach': tmpAttach, 'sTitle': i['title'], 'top': i['top']})
            # 排序
        self.__cacheContent.sort(key=functools.cmp_to_key(self.__cmpDatetime))

    def freshCache(self):
        # 首先需要复制原有缓存
        oldCache = self.__cacheList.copy()
        # 重新创建列表缓存
        self.createListCache()
        # 批量比较不同，将不同的内容放入缓存前方
        # 首先进行快比较
        if operator.eq(self.__cacheList, oldCache):
            self.l.notice("缓存未更改！")
            return None
        else:
            k = 0
            newCache = []
            # 创建新缓存
            self.createContentCache()
            for i in self.__cacheContent:
                for j in oldCache:
                    if i['sTitle'] != j['title']:
                        newCache.append(i)
                        k += 1
            for i in range(1, k):
                self.__cacheContent.pop()
            self.l.info("共删除%d条。" % k)
            # return newCache
            self.__cacheContent.append(newCache)
            # 此处需要排序，否则会出错
            self.__cacheContent.sort(key=functools.cmp_to_key(self.__cmpDatetime))
            return newCache

    def get(self):
        return self.__cacheContent
