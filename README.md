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
1. Package `GetAnnounce`负责获取通知内容
    1. `GetAnnounce.init()`，初始化方法，可传入文本型通知域名/IP，该方法会尝试连接传入地址（默认oa.jlu.edu.cn），若无法连接则抛出NetworkError异常。
    2. `GetAnnounce.createCache()`，创建页面缓存，该页面缓存**不会**自动更新，需要通过`GetAnnounce.freshCache()`方法进行刷新，同样会抛出NetworkError异常。
    3. `GetAnnounce.freshCache()`，刷新页面缓存，同样会抛出NetworkError异常。
      
    需要注意的是，该页面缓存有且仅有一个，缓存数量为5并且缓存内容为{"网址":"HTML文本"}。
    4. `GetAnnounce.get()`，返回缓存中的前5条。
    
2. Package `ProcessText`负责文本处理