import Logger
import requests
from lxml import etree

class GetAnnounce:
    __domain = ""
    __direct = "defaultroot/"
    __list = "PortalInformation!jldxList.action?channelId=179577"
    __cacheList = []
    __cacheContent = []

    l  = Logger.Logger()
    def __testHttp(self,target):
        try:
            self.l.info("正在测试网络连通...")
            return requests.get(target)
        except:
            return False

    def __process(self):
        return " "

    def __init__(self, text):
        if text == "" or text == " ":
            self.__domain = "https://oa.jlu.edu.cn/"
        else:
            self.__domain = text
        if self.__testHttp(self.__domain):
            self.l.notice("Http连接成功！")
            self.l.info("目标地址："+self.__domain)
        else:
            self.l.error("连接错误！请检查网络连接！")
            raise Exception("NetworkError")


    def createCache(self):
        self.l.info("正在获取网页内容...")
        html = requests.get(self.__domain+self.__direct+self.__list).text
        self.l.notice("获取成功！")
        data = etree.HTML(html)
        for i in range(1,31):
            title = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/text()' % i)
            time = data.xpath('//*[@id="itemContainer"]/div[%d]/span/text()' % i)
            href = data.xpath('//*[@id="itemContainer"]/div[%d]/a[1]/@href' % i)
            author = data.xpath('//*[@id="itemContainer"]/div[%d]/a[2]/text()' % i)
            self.l.info("获取到《%s》通知" % title[0])
            self.__cacheList.append({"title":title[0],"time":time[0],"href":self.__domain+href[0],"author":author[0]})


        '''
        #TODO
        对时间进行排序
        什么的，得到一个排序后的列表，然后根据列表进行内容抓取，放到__cacheContent里面，就可以了。
        '''
        for i in self.__cacheList:
            self.l.info("正在获取《%s》..." % i['title'])
            html = requests.get(self.__domain + self.__direct + i['href']).text
            self.l.notice("获取成功！")
            content = data.xpath('/html/body/div[3]/div[1]/div[2]/div[2]/div/div[3]/div/div[3]/p[25]/span/span//text()')
            print(content)




