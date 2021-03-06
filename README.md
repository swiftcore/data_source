data_source工具使用说明
===============

简介
-------------

这是一个获取股票数据的应用

实时数据获取
--------------- 

### 功能和设计

实时数据获取工具利用Wind的个人量化工具WindPy，从Wind服务器实时获取股票的tick数据信息，得到tick后，将数据存储在服务器端的内存中。

服务器采用XMLRPC实现，如果想要取得已经得到的某只股票的所有tick或一些tick进行相关的衍生计算，可以直接调用服务器的远程方法。

客户端中包含了从Wind服务器获取数据的功能（fetch.py中），获得数据后，会调用服务器的远程方法，将数据存储到服务器端。

### 使用步骤

1. 启动服务器

``` bash
cd server
python server.py log.txt
``` 

2. 启动客户端

``` bash 
cd client 
python fetch.py connection.txt
``` 

3. 停止服务器或客户端

> 直接按Control+C终端程序执行


注意事项：
----------------- 
如果你没有Wind账号，请到如下地址下载软件并注册账号

http://www.windin.com/windin2/Index.htm 

同时，下载量化个人接口

http://www.dajiangzhang.com/download

启动量化个人接口后，选择小框中的记住用户名和密码，这样每次获取数据的时候就不会总问你密码了。
