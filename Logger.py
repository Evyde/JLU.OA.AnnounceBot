class Logger(object):
    instance = None
    initFlag = False
    isClose = False

    def __write(self, text):
        if self.isClose is False:
            print(text)

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if Logger.initFlag:
            return
        Logger.init_flag = True

    def error(self, text):
        self.__write("\033[0;31;40m[ERROR] " + str(text) + "\033[0m")
        return

    def notice(self, text):
        self.__write("\033[0;33;40m[NOTICE] " + str(text) + "\033[0m")
        return

    def info(self, text):
        self.__write("\033[0;32;40m[INFO] " + str(text) + "\033[0m")
        return
