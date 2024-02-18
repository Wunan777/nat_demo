#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
import socket  # 导入 socket 模块
from src.socket_helper import recvall

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"  # 获取本地主机名
port = 8111  # 设置端口
print("{}:{}".format(host, port))
s.bind((host, port))  # 绑定端口

s.listen(5)  # 等待客户端连接
while True:
    c, addr = s.accept()  # 建立客户端连接
    print("connect add: {}".format(addr))

    while True:
        recv_data = recvall(c)
        print(recv_data)
        msg = "server reply: recv : {}.".format(recv_data.decode())
        c.send(msg.encode())
