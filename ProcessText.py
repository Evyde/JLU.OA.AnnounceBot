class ProcessText:
    __cache = {}
    __result = {}

    def __init__(self, text):
        self.__cache = text

    def getSimpleText(self):
        self.__result['title'] = self.__cache['title']
        self.__result['content'] = str(self.__cache['content'])[0:50]
        return self.__result

    def getNormalText(self):
        self.__result['title'] = self.__cache['title']
        self.__result['content'] = str(self.__cache['content'])
        return self.__result

    def getFullTextMD(self):
        self.__result['title'] = self.__cache['title']
        tmp = "# " + self.__result['title'] + "\n  \n"
        tmp += "## 日期： **" + self.__cache['time']
        tmp += "**  作者： **" + self.__cache['author'] + "**\n  \n  ---  \n  \n"
        tmp += self.__cache['content']
        tmp += "\n  ---  \n  "
        if 'attach' in self.__cache:
            for i in self.__cache['attach']:
                for k in i:
                    tmp += "## 附件：" + "[%s]" % k
                    tmp += "(%s)\n  \n" % i.get(k)
        self.__result['content'] = tmp
        return self.__result

    def getFullText(self):
        self.__result['title'] = self.__cache['title']
        tmp = self.__result['title'] + "\n"
        tmp += "日期：" + self.__cache['time']
        tmp += "作者：" + self.__cache['author'] + "**\n"
        tmp += self.__cache['content']
        tmp += "\n"
        if 'attach' in self.__cache:
            for i in self.__cache['attach']:
                for k in i:
                    tmp += "附件：" + "%s:" %k
                    tmp += "%s\n" % i.get(k)
        self.__result['content'] = tmp
        return self.__result
