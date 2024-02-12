import asyncio
import socket
from threading import Thread
import time
import select
from flask import Flask, request


def create_socket_send_and_recv(data):
    s = socket.socket()  # 创建 socket 对象
    host = "127.0.0.1"  # 获取本地主机名
    port = 8113  # 设置端口号

    s.connect((host, port))
    # print(s.recv(1024))
    s.sendall(data)
    res = s.recv(1024)
    return res


def handle_request(client_socket):
    request_data = client_socket.recv(1024)
    # 解析HTTP请求头
    headers = request_data.decode().split("\r\n")
    if headers:
        request_line = headers[0]
        method, path, protocol = request_line.split(" ")
        print(method, path, protocol)

        response = create_socket_send_and_recv(request_data)
        # 返回HTTP响应
        # response = (
        #     "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello, World!</h1>"
        # )
        client_socket.sendall(response)

    client_socket.close()


def createHttpProxySocket(ip, port):
    print("HttpProxy: '{}:{}', running...".format(ip, port))
    # await run_server(ip, port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    # while True:
    #     print("waiting...")
    #     client_socket, addr = server_socket.accept()
    #     print(f"Connection from {addr}")
    #     handle_request(client_socket)

    return server_socket


app = Flask(__name__)


@app.route("/proxy", methods=["POST"])
def post_example():
    # 获取 POST 请求中的数据
    data = request.form.get("data")
    return f"POST 请求数据：{data}"


def run_flask():
    app.run(debug=True, port=8080)


if __name__ == "__main__":

    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    flask_thread.join()
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server_socket.bind(("", 8811))
    # server_socket.listen(5)
    s1 = createHttpProxySocket("127.0.0.1", 8811)
    s2 = createHttpProxySocket("127.0.0.1", 8822)

    server_list = [s1, s2]
    # List will be read.
    read_list = [s1, s2]

    while True:
        readable, writable, errored = select.select(read_list, [], [])

        for s in readable:
            if s in server_list:
                client_socket, address = s.accept()
                read_list.append(client_socket)
                print("Connection from: {}".format(address))
            else:
                # data = s.recv(1024)
                handle_request(s)
                read_list.remove(s)
