import socket


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


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(5)

    print("Listening on port 8080...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        handle_request(client_socket)


if __name__ == "__main__":
    run_server()
