class Logger(object):
    def __write(self,text):
        print(text)


    instance = None
    initFlag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if Logger.initFlag:
            return
        Logger.init_flag = True

    def error(self,text):
        self.__write("[ERROR] " + text)


    def notice(self,text):
        self.__write("[NOTICE] " + text)


    def info(self,text):
        self.__write("[INFO] " + text)