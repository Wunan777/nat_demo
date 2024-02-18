import os
import socket
import argparse
from src.const import RECV_MAX_SIZE


def create_proxy_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (host, port)
    s.connect(address)
    return s


def connect_nat_server(host, port):
    # 创建一个TCP/IP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接套接字到服务器端
    address = (host, port)
    s.connect(address)
    return s


def main():
    # 获取环境变量
    nat_server = os.environ.get("NAT_SERVER")
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(description="NAT Client")
    parser.add_argument("--type", help="Type of connection", required=True)
    parser.add_argument(
        "--local_port", type=int, help="Local port number", required=True
    )
    parser.add_argument(
        "--remote_port", type=int, help="Remote port number", required=True
    )
    args = parser.parse_args()

    # 打印获取到的值
    print("NAT Server:", nat_server)
    print("Type:", args.type)
    print("Local Port:", args.local_port)
    print("Remote Port:", args.remote_port)

    # 1, `proxy socket` to `local server`.
    # proxy_socket = create_proxy_socket(host="127.0.0.1", port=args.local_port)

    # 2, Conn `nat server` with socket.
    nat_server_host, nat_server_port = nat_server.split(":")
    nat_server_port = int(nat_server_port)
    nat_server_socket = connect_nat_server(
        host=nat_server_host,
        port=nat_server_port,
    )
    # 3, Request Register `remote_port` on `nat_server`.
    message = "{};{};{}".format("register", args.type, args.remote_port)
    nat_server_socket.sendall(message.encode())

    # 4,
    while True:
        try:
            # # 发送消息到服务器端
            # message = input("请输入要发送的消息: ")
            # client_socket.sendall(message.encode())

            # # 接收来自服务器端的响应
            # print("收到来自服务器端的响应:", response.decode())
            r1 = nat_server_socket.recv(RECV_MAX_SIZE)
            proxy_socket = create_proxy_socket(host="127.0.0.1", port=args.local_port)
            proxy_socket.sendall(r1)
            r2 = proxy_socket.recv(RECV_MAX_SIZE)
            print("data: {}".format(r2))
            print("Start: send data to nat server...")
            nat_server_socket.sendall(r2)
            print("Finished: send data to nat server.")
        except socket.error as err:
            print("error: {}".format(err))
            proxy_socket = connect_nat_server(host="127.0.0.1", port=args.local_port)

        finally:
            # client_socket.close()
            pass


if __name__ == "__main__":
    main()
