class Logger(object):
    __instance = None
    __initFlag = False
    __isClose = False
    __method = "console"
    __filePointer = None

    def __write(self, text):
        if self.__isClose is False:
            if self.__method == "console":
                print(text)
            elif self.__method == "file":
                self.__filePointer.write(text)

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, method):
        if Logger.__initFlag:
            return
        if method == "" or method == " " or method != "file":
            pass
        else:
            self.__method = str(method).lower()
        if self.__method == "file":
            self.__filePointer = open("./announcebot.log", 'a', encoding='utf-8')
        Logger.__initflag = True

    def setMethod(self, method):
        self.__method = str(method).lower()
        if self.__method == "file" and self.__filePointer == None:
            self.__filePointer = open("./announcebot.log", 'a', encoding='utf-8')

    def error(self, text):
        self.__write("\033[0;31;40m[ERROR] " + str(text) + "\033[0m")
        return

    def notice(self, text):
        self.__write("\033[0;33;40m[NOTICE] " + str(text) + "\033[0m")
        return

    def info(self, text):
        self.__write("\033[0;32;40m[INFO] " + str(text) + "\033[0m")
        return
