import GetAnnounce, MessageSender, Logger, ProcessText, time

def main():
    l = Logger.Logger()
    methodFlag = True
    while methodFlag:
        l.info("欢迎使用校内通知接收机器人！")
        l.info("支持3种接收消息方法：")
        l.info("1. ServerChan")
        l.info("2. SMTP邮件")
        l.info("3. 控制台")
        l.notice("请输入接收通知方法[1,2,3]：")
        userInput = int(input())
        if userInput is 1:
            m = MessageSender.MessageSender("serverchan")
            l.notice("请输入您的SCKEY：")
            SCKEY = input()
            m.config({'SCKEY': SCKEY})
            methodFlag = False
            # 'SCU59621Tfe85588030e0a45116714e3b47fd35d85d74d3e91354b'
        elif userInput is 2:
            m = MessageSender.MessageSender("smtp")
            l.notice("请分别输入您的主机IP或域名、端口、用户名、密码、用以发送的邮箱、接收邮箱、发送者名称及接收者名称。")
            host = input("Host:")
            port = input("Port:")
            user = input("User:")
            pwd = input("Password:")
            fromAddr = input("FromAddr:")
            toAddr = input("toAddr:")
            fromName = input("fromName:")
            toName = input("toName:")
            m.config({"host": host, "port": port, "fromAddr": fromAddr,
                      "toAddr": toAddr, "fromName": fromName,
                      "toName": toName, "user": user, "pwd": pwd})
            methodFlag = False
        elif userInput is 3:
            m = MessageSender.MessageSender("console")
            m.config({})
            methodFlag = False
        else:
            l.error("输入错误！请重新输入")

    g = GetAnnounce.GetAnnounce("")

    g.createCache()
    cache = g.get()
    for i in cache:
        p = ProcessText.ProcessText(i)
        if m.getMethod() == "serverchan":
            l.notice(m.send(p.getFullTextMD()))
        elif m.getMethod() == "smtp":
            l.notice(m.send(p.getFullText()))
        elif m.getMethod() == "console":
            l.notice(m.send(p.getSimpleText()))
        time.sleep(1)
    while True:
        cache = g.freshCache()
        if cache != None:
            for i in cache:
                p = ProcessText.ProcessText(i)
                l.notice(m.getMethod())
                if m.getMethod() == "serverchan":
                    l.notice(m.send(p.getFullTextMD()))
                elif m.getMethod() == "smtp":
                    l.notice(m.send(p.getFullText()))
                elif m.getMethod() == "console":
                    l.notice(m.send(p.getSimpleText()))
                time.sleep(1)
        # 回收资源
        del p
        # 休息5分钟
        l.info("5分钟后重试")
        time.sleep(300)

main()
