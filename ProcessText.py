class ProcessText:
    __cache = {}
    __result = {}

    def __init__(self, text):
        self.__cache = text

    def getSimpleText(self):
        self.__result['title'] = self.__cache['top'] + " " + self.__cache['title']
        self.__result['content'] = self.__cache['title'] + "\n" + str(self.__cache['content'])[0:20]
        return self.__result

    def getNormalText(self):
        self.__result['title'] = self.__cache['top'] + " " + self.__cache['title']
        self.__result['content'] = str(self.__cache['content'])
        return self.__result

    def getFullTextMD(self):
        self.__result['title'] = self.__cache['title']
        tmp = "## " + self.__cache['top'] + " " + self.__result['title'] + "\n  \n"
        tmp += "### 日期： **" + self.__cache['time']
        tmp += "**  作者： **" + self.__cache['author'] + "**\n  \n  ---  \n  \n"
        tmp += self.__cache['content']
        tmp += "\n  ---  \n  "
        if self.__cache['attach']:
            for i in self.__cache['attach']:
                tmp += "### 附件：" + "[%s]" % i
                tmp += "(%s)\n  \n" % self.__cache['attach'].get(i)
        else:
            tmp += "### 该通知没有附件。"
        self.__result['content'] = tmp
        return self.__result

    def getFullText(self):
        self.__result['title'] = self.__cache['title']
        tmp = self.__cache['top'] + " " + self.__result['title'] + "\n"
        tmp += "日期：" + self.__cache['time']
        tmp += "作者：" + self.__cache['author'] + "\n"
        tmp += 50 * '-'
        tmp += "\n"
        tmp += self.__cache['content']
        tmp += "\n"
        tmp += 50 * '-'
        tmp += "\n"
        if self.__cache['attach']:
            for i in self.__cache['attach']:
                tmp += "附件：" + "%s:" % i
                tmp += "%s\n" % self.__cache['attach'].get(i)
        else:
            tmp += "该通知没有附件！"
        self.__result['content'] = tmp
        return self.__result
