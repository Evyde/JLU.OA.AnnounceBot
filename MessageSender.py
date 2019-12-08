import requests
from urllib import parse
class MessageSender(object):
    __method = "ServerChan"
    __sender = None

    def __init__(self,method):
        self.__method = str(method)
        self.__method = self.__method.lower()


    def config(self,config):
        if self.__method == "serverchan":
            self.__sender = ServerChan(config)
        elif self.__method == "smtp":
            self.__sender = SMTPSender(config)
        else:
            raise Exception("Configure Exception")


    def send(self,msg):
        if self.__method == "serverchan":
            self.__sender.send(msg)
        elif self.__method == "smtp":
            self.__sender.send(msg)
        else:
            raise Exception("Configure Exception")


class ServerChan(object):
    __sckey = ""
    def __init__(self,SCKEY):
        self.__sckey = SCKEY['SCKEY']


    def send(self,msg):
        url = "https://sc.ftqq.com/"+ self.__sckey +".send?text=" + parse.quote(msg['title']) + "&desp=" + parse.quote(msg['content'])
        return requests.get(url)


class SMTPSender(object):
    def xxx(self):
        return


