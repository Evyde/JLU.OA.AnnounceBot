from email.header import Header
from email.mime.text import MIMEText
from urllib import parse
import requests, smtplib


class MessageSender(object):
    __method = "ServerChan"
    __sender = None
    __obj = None
    initFlag = False

    def __new__(cls, *args, **kwargs):
        if cls.__obj is None:
            cls.__obj = super().__new__(cls)
        return cls.__obj

    def __init__(self, method):
        if self.initFlag is False:
            self.__method = str(method)
            self.__method = self.__method.lower()
        self.initFlag = True

    def config(self, config):
        if self.__method == "serverchan":
            self.__sender = ServerChan(config)
        elif self.__method == "smtp":
            self.__sender = SMTPSender(config)
        elif self.__method == "console":
            self.__sender = ConsoleSender(config)
        else:
            raise Exception("Configure Exception")

    def send(self, msg):
        try:
            return self.__sender.send(msg)
        except:
            raise Exception("Configure Exception")

    def getMethod(self):
        return self.__method


class ServerChan(object):
    __sckey = ""

    def __init__(self, SCKEY):
        self.__sckey = SCKEY['SCKEY']

    def send(self, msg):
        url = "https://sc.ftqq.com/" + self.__sckey + ".send?text=" + parse.quote(
            msg['title']) + "&desp=" + parse.quote(msg['content'])
        return "发送状态：" + str(requests.get(url))


class SMTPSender(object):
    __configList = {}
    __smtpObj = None

    def __init__(self, list):
        self.__configList = list
        self.__smtpObj = smtplib.SMTP_SSL(self.__configList['host'], self.__configList['port'])

    def send(self, msg):
        message = MIMEText(msg['content'], 'plain', 'utf-8')
        message['From'] = self.__configList['fromName']
        message['To'] = self.__configList['toName']
        message['Subject'] = Header(msg['title'], 'utf-8')
        self.__smtpObj.connect(self.__configList['host'])
        self.__smtpObj.ehlo(self.__configList['host'])
        self.__smtpObj.login(self.__configList['user'], self.__configList['pwd'])
        self.__smtpObj.sendmail(self.__configList['fromAddr'], self.__configList['toAddr'], message.as_string())
        return "已向%s发送邮件，请查收！" % self.__configList['toAddr']


class ConsoleSender(object):
    def __init__(self, config):
        config = config

    def send(self, msg):
        print("《%s》" % msg['title'])
        print(msg['content'])
        return "控制台输出成功！"
