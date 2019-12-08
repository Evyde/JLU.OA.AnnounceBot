class ProcessText:
    __cache = []
    __result = []

    def __processText(self):
        return " "

    def set(self,text):
        if len(text) == 0:
            raise Exception("NULLPointerException")
        self.__cache = text.items()[0]
        self.__processText()

    def get(self):
        return self.__result


    def link(self):
        return str(self.__result['attach']).split("@@@")


    def getMD(self):
        return "MD"



