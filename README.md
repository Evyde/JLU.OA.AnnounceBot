# 吉林大学校内通知获取机器人
- 作者：Evyde（ForeverOpp）

---
## 项目功能
1. 实现校内通知的自动获取
2. 将通知内容及标题通过ServerChan推送至微信或SMTP发送至邮箱或通过Bark推送或本地输出。
3. 对于附件，则附上链接
  
## 已知问题
1. 缓存更新时，会出现错误，具体是更新完列表之后，不知道怎么回事会出现列表中的列表，我设计的时候默认是列表套字典的，所以访问会出现问题。


## 使用原理与技术
1. 爬虫
2. HTTP GET POST
3. 文本处理

  
## 使用的第三方库
1. lxml
2. requests
  
  
## 使用的Python自带库
1. time
2. datetime
3. operator
4. functools
5. email
6. urllib
7. smtplib


## 结构
1.  Class `GetAnnounce`负责获取通知内容
    1. `GetAnnounce.__init__(text, logger)`，初始化方法，可传入文本型通知域名/IP，该方法会尝试连接传入地址（传入""或" "则默认oa.jlu.edu.cn），若无法连接则抛出NetworkError异常，`logger`则为通知类引用。
    2. `GetAnnounce.createListCache`，创建标题列表缓存，该页面缓存**不会**自动更新，需要通过`GetAnnounce.freshCache()`方法进行刷新，同样会抛出NetworkError异常。
    3. `GetAnnounce.freshCache()`，刷新页面和标题列表缓存，同样会抛出NetworkError异常。。
    4. `GetAnnounce.get()`，返回缓存。
    5. `GetAnnounce.getContentCache(target)`，按照指定的列表缓存获取内容，返回一个列表。
    6. `GetAnnounce.createContentCache()`，创建内容缓存，该方法仅第一次创建缓存时使用，更新缓存时不采用。 
   
2.  Class `ProcessText`负责处理发送的消息
    1. `ProcessText.__init__(text)`，初始化方法，传入一个字典。
    2. `ProcessText.getNormalText()`，返回一个只有标题和完整内容的字典，没有作者等信息。
    3. `ProcessText.getFullText()`，返回一个加入作者等信息的字典。
    4. `ProcessText.getSimpleText()`，返回一个只有标题、作者和30字摘要的字典。
    5. `ProcessText.getFullTextMD()`，返回一个加入作者等信息，且少量内容使用Markdown格式化后的字典。
    
3.  Class `MessageSender`负责消息发送
    
    该类可扩展，故设置了一个`__init__(method)`方法用以选择发送方法，支持smtp邮件发送，ServerChan微信推送，控制台输出和iOS端的软件Bark推送，关于ServerChan的介绍，请移步[ServerChan](http://sc.ftqq.com)，关于Bark的介绍，请移步[Bark](https://github.com/Finb/Bark/)。
    1. `MessageSender.__init__(method)`，该方法传入一个`method`文本，可从`serverChan`、`smtp`、`console`、`Bark`中选一个。
    2. `MessageSender.config(config)`，该方法传入一个`config`字典，以下是两种方式的配置字典格式：
        1.  ServerChan
            
            格式：`{"SCKEY":"你的SCKEY"}`。
            
        2.  SMTP
            
            格式：`{"host":"主机IP或域名","port":"端口，一般是25","fromAddr":"用以发送的邮箱","toAddr":"接收邮箱","fromName":"发送者名称","toName":"接收者名称", "user": "用户名", "pwd": "密码"}`。
         
        3.  Console
            无需配置，config方法直接return
            
        4. Bark
            格式：`{"apiKey": "你的APIKEY"}`
    3. `MessageSender.send(msg)`，发送消息，发送失败会在控制台输出日志，不会抛出异常。
    4. `MessageSender.getMethod()`，返回发送的方法。
    
4.  Class `ServerChan`负责向ServerChan发送消息。
    1. `ServerChan.__init__(text)`，传入SCKEY。
    2. `ServerChan.send(msg)`，发送消息（支持Markdown格式），直接返回发送状态。
    
5.  Class `SMTPSender`负责通过SMTP发送消息。
    1. `SMTPSender.__init__(list)`，传入上述配置字典。
    2. `SMTPSender.send(msg)`，发送消息，直接返回发送成功的文本。
    
6.  Class `ConsoleSender`负责通过控制台输出消息。
    1. `ConsoleSender.send(msg)`，发送消息，直接返回发送成功的文本。
    
7.  Class `BarkSender`负责通过Bark发送消息。
    1. `BarkSender.__init__(apikey)`，传入APIKEY。
    2. `BarkSender.send(msg)`，发送消息，直接返回发送状态。
    
8.  Class `Logger`负责生成日志。
   
    该类中，有三大消息类型，分别是Error、Notice、Info。
    同时，如果需要关闭日志，请将isClose设置为True。另外，可以选择控制台或者文件输出。    
    1. `Logger.__init__()`，初始化，可扩展。
    2. `Logger.error(text)`，向日志中写入一条内容为text的Error类型消息。
    3. `Logger.notice(text)`，向日志中写入一条内容为text的Notice类型消息。
    4. `Logger.info(text)`，向日志中写入一条内容为text的Info类型消息。
    5. `Logger.__write(text)`，向日志中写入消息，无需用户自行调用。
