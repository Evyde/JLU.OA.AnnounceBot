import GetAnnounce
import Logger
import MessageSender
import ProcessText
import configparser
import time


def chkUserInput(userInput):
    if userInput == "y" or userInput == "Y" or userInput == "":
        return True
    else:
        return False


def getCfgs(cfg, configs, section, l):
    rtnList = {}
    if section in cfg.sections():
        for i in configs:
            if i not in cfg.options(section):
                return None
            rtnList.update({i: cfg.get(section, i)})
        l.notice("检测到配置文件，请问是否使用？[Y/n]：")
        if chkUserInput(input()):
            return rtnList
        else:
            return None
    else:
        cfg.add_section(section)
        return None


def setCfgs(cfg, configs, section):
    for k, v in configs.items():
        cfg.set(section, k, v)
    return cfg


def main():
    l = Logger.Logger("")
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    methodFlag = True
    while methodFlag:
        l.info("欢迎使用校内通知接收机器人！")
        l.info("支持4种接收消息方法：")
        l.info("1. ServerChan")
        l.info("2. SMTP邮件")
        l.info("3. 控制台")
        l.info("4. iOS端的Bark应用")
        l.notice("请输入接收通知方法[1,2,3,4]：")
        userInput = int(input())
        if userInput == 1:
            m = MessageSender.MessageSender("serverchan")
            tmp = getCfgs(cfg, ["SCKEY"], "serverchan", l)
            if tmp is not None:
                m.config(tmp)
                break
            l.notice("请输入您的SCKEY：")
            SCKEY = input()
            cfgDict = {'SCKEY': SCKEY}
            m.config(cfgDict)
            cfg = setCfgs(cfg, cfgDict, "servserchan")
            methodFlag = False
        elif userInput == 2:
            m = MessageSender.MessageSender("smtp")
            tmp = getCfgs(cfg, ["host", "port", "fromAddr", "toAddr", "fromName", "toName", "user", "pwd"], "smtp", l)
            if tmp is not None:
                m.config(tmp)
                break
            l.notice("请分别输入您的主机IP或域名、端口、用户名、密码、用以发送的邮箱、接收邮箱、发送者名称及接收者名称。")
            host = input("Host:")
            port = input("Port:")
            user = input("User:")
            pwd = input("Password:")
            fromAddr = input("FromAddr:")
            toAddr = input("toAddr:")
            fromName = input("fromName:")
            toName = input("toName:")
            cfgDict = {"host": host, "port": port, "fromAddr": fromAddr,
                       "toAddr": toAddr, "fromName": fromName,
                       "toName": toName, "user": user, "pwd": pwd}
            m.config(cfgDict)
            cfg = setCfgs(cfg, cfgDict, "smtp")
            methodFlag = False
        elif userInput == 3:
            m = MessageSender.MessageSender("console")
            m.config({})
            methodFlag = False
        elif userInput == 4:
            m = MessageSender.MessageSender("bark")
            tmp = getCfgs(cfg, ["apikey"], "bark", l)
            if tmp is not None:
                m.config(tmp)
                break
            l.notice("请输入您的APIKEY：")
            SCKEY = input()
            cfgDict = {'apikey': SCKEY}
            m.config(cfgDict)
            cfg = setCfgs(cfg, cfgDict, "bark")
            methodFlag = False
            # x5Pza5ihMyZCkFpW28D6KY
        else:
            l.error("输入错误！请重新输入")
    l.info("请选择日志输出方式（默认控制台）:")
    l.info("1. 控制台")
    l.info("2. 文件announcebot.log")
    l.notice("请输入：")
    userInput = int(input())
    if userInput == 2:
        l.setMethod("file")
    with open("config.ini", encoding="utf-8", mode='w+') as fp:
        cfg.write(fp)
    g = GetAnnounce.GetAnnounce("", l, cfg)
    while True:
        for i in g.get():
            p = ProcessText.ProcessText(i)
            l.notice(m.getMethod())
            if m.getMethod() == "serverchan":
                l.notice(m.send(p.getFullTextMD()))
            elif m.getMethod() == "smtp":
                l.notice(m.send(p.getFullText()))
            elif m.getMethod() == "console":
                l.notice(m.send(p.getNormalText()))
            elif m.getMethod() == "bark":
                l.notice(m.send(p.getSimpleText()))
            # time.sleep(1)
        # 休息5分钟
        l.info("5分钟后重试")
        with open("config.ini", encoding="utf-8", mode='w+') as fp:
            cfg.write(fp)
        time.sleep(300)


main()
