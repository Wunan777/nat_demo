import socket

# 创建一个TCP/IP套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定套接字到端口
server_address = ("localhost", 8001)
server_socket.bind(server_address)

# 开始监听传入的连接
server_socket.listen(1)

print("等待客户端连接...")

# 等待客户端连接
client_socket, client_address = server_socket.accept()
print(f"已连接到客户端: {client_address}")

try:
    while True:
        # 接收来自客户端的消息
        data = client_socket.recv(1024)
        if data:
            print("收到来自客户端的消息:", data.decode())
            # 发送响应到客户端
            response = input("请输入响应消息: ")
            client_socket.sendall(response.encode())
        else:
            print("客户端关闭了连接")
            break
finally:
    # 清理连接
    client_socket.close()
    server_socket.close()
