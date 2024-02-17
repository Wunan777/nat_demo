#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
import socket  # 导入 socket 模块
from src.Socket import Socket

s = Socket()  # 创建 socket 对象
host = "127.0.0.1"  # 获取本地主机名
port = 8111  # 设置端口
print("{}:{}".format(host, port))
s.bind((host, port))  # 绑定端口

s.listen(5)  # 等待客户端连接
while True:
    c, addr = s.accept()  # 建立客户端连接
    print("connect add: {}".format(addr))
    c.send(b"Hi, I am sever.")
    c.close()  # 关闭连接
