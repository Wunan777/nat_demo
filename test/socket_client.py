import socket

# 创建一个TCP/IP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接套接字到服务器端
server_address = ("127.0.0.1", 8822)
client_socket.connect(server_address)

try:
    while True:
        # 发送消息到服务器端
        message = input("请输入要发送的消息: ")
        client_socket.sendall(message.encode())

        # 接收来自服务器端的响应
        response = client_socket.recv(1024)
        print("收到来自服务器端的响应:", response.decode())
finally:
    # 关闭套接字
    client_socket.close()
