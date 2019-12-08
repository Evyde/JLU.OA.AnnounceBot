# Python期末作业
- 作者：韩枫
  
- 学号：24190707
  
---
## 项目功能
1. 实现校内通知的自动获取
2. 将通知内容及标题通过ServerChan推送至微信
3. 对于附件，则使用上传某临时空间做外链（该功能可暂时不做）

## 使用原理与技术
1. 爬虫
2. HTTP GET POST
3. 文本处理

## 结构
1. [ ] Class `GetAnnounce`负责获取通知内容
    1. `GetAnnounce.__init__(text)`，初始化方法，可传入文本型通知域名/IP，该方法会尝试连接传入地址（传入""或" "则默认oa.jlu.edu.cn），若无法连接则抛出NetworkError异常。
    2. `GetAnnounce.createCache()`，创建页面缓存，该页面缓存**不会**自动更新，需要通过`GetAnnounce.freshCache()`方法进行刷新，同样会抛出NetworkError异常。
    3. `GetAnnounce.freshCache()`，刷新页面缓存，同样会抛出NetworkError异常。需要注意的是，该页面缓存有且仅有一个，缓存数量为20并且缓存内容为`{"address":"网址","html":"网页内容"}`。
    4. `GetAnnounce.get()`，返回缓存中的前20条。
    
2. [ ] Class `ProcessText`负责文本处理
    
    该类有一个字典变量，但是不可被访问，和`GetAnnounce`类似，有`get()`方法。
    1. `ProcessText.set(text)`，设置该字典变量的值，该方法会对传入的字典长度进行验证，如果大于1则丢弃后面的内容。另外该方法会自动调用`__processText()`方法进行文本处理，用户无需自行调用。
    2. `ProcessText.get()`，返回处理后的字典（普通格式），该字典长度为4，而附件网址之间用`@@@`分隔，需要用户调用`ProcessText.link()`方法处理，该字典格式为：`{"title":"标题","time":"时间","text":"正文内容","attach":"附件链接1@@@附件链接2"}`。
    3. `ProcessText.link()`，返回处理后的链接，内容为字典,格式`{"attach1":"网址","attach2":"网址",...}`如果没有附件，则返回Null。
    4. `ProcessText.getMD()`，返回处理后的字典（Markdown格式），字典格式同`get()`方法。
    5. `ProcessText.__processText()`方法，处理文本并将处理好的字典储存在`__result`中。
    
3. [ ] Class `MessageSender`负责消息发送
    
    该类可扩展，故设置了一个`__init__(method)`方法用以选择发送方法，拟加入smtp邮件发送，目前只有ServerChan发送，关于ServerChan的介绍，请移步[ServerChan](http://sc.ftqq.com)。
    1. `MessageSender.__init__(method)`，该方法传入一个`method`文本，可从`serverChan`、`smtp`中选一个（虽然目前只有serverChan)。
    2. `MessageSender.config(config)`，该方法传入一个`config`字典，以下是两种方式的配置字典格式：
        1. [ ] ServerChan
            
            格式：`{"SCKEY":"你的SCKEY"}`。
            
        2. [ ] SMTP
            
            格式：`{"host":"主机IP或域名","port":"端口，一般是25","fromAddr":"用以发送的邮箱","toAddr":"接收邮箱","fromName":"发送者名称","toName":"接收者名称"}`。
            
    3. `MessageSender.send()`，发送消息，发送失败会在控制台输出日志，不会抛出异常。
    
4. [ ] Class `ServerChan`负责向ServerChan发送消息。
    1. `ServerChan.__init__(text)`，传入SCKEY。
    2. `ServerChan.send(msg)`，发送消息（支持Markdown格式），失败返回错误文本。
    
5. [ ] Class `SMTPSender`负责通过SMTP发送消息。
    1. `SMTPSender.__init__(list)`，传入上述配置字典。
    2. `SMTPSender.send()`，发送消息，直接返回发送成功的文本。
    
6. [ ] Class `Logger`负责生成日志。
   
    该类中，有三大消息类型，分别是Error、Notice、Info。    
    1. `Logger.__init__()`，未来会实现对文件/数据库的写入。
    2. `Logger.error(text)`，向日志中写入一条内容为text的Error类型消息。
    3. `Logger.notice(text)`，向日志中写入一条内容为text的Notice类型消息。
    4. `Logger.info(text)`，向日志中写入一条内容为text的Info类型消息。
    5. `Logger.__write(text)`，向日志中写入消息，无需用户自行调用。