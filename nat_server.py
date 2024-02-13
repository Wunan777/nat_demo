import socket
import select

proxy_port_map = {}
# The `server socket` and `proxy socket` need to be persistent.
server_socket_list = []
proxy_socket_list = []
# The socket which `server socket` created directly or  indirectly, should put into the `read socket` list.
read_socket_list = []


def createHttpProxySocket(ip, port):
    print("HttpProxy: '{}:{}', running...".format(ip, port))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    return server_socket


def handle_register_request(data: bytes):
    # example: 'register;http;8811'
    message = data.decode()
    if not message:
        raise Exception("handle_register_request err: no data")

    flag_filed, proxy_type, remote_port = message.split(";")
    if proxy_type == "http":
        port = int(remote_port)
        proxy_server = createHttpProxySocket(ip="127.0.0.1", port=port)
        return proxy_type, remote_port, proxy_server
    else:
        raise Exception("unvalid proxy_type : {}".format(proxy_type))


def handle_http_request(req_port, req_data):
    s = proxy_port_map[req_port]["channel_socket"]
    s.sendall(req_data)
    res = s.recv(1024)
    return res


def handle_request(client_socket):
    request_data = client_socket.recv(1024)
    if not request_data:
        print("client socket close, {}".format(client_socket))
        client_socket.close()

    try:
        # 解析HTTP请求头
        # HTTP/1.1 200 OK
        # Server: nginx
        # Content-Type: text/html
        # Content-Length: 12
        request_lines = request_data.decode().split("\r\n")
        request_line = request_lines[0]
        if "HTTP" in request_line:
            # [
            #     "GET / HTTP/1.1",
            #     "Host: 127.0.0.1:8812",
            #     "Connection: keep-alive",
            #     "Cache-Control: max-age=0",
            # ]
            print("handle http request. {}".format(request_lines))
            header = request_lines[0]
            host_info = request_lines[1]

            method, path, protocol = header.split(" ")
            print(method, path, protocol)
            request_port = host_info.split(":")[-1]
            res = handle_http_request(request_port, request_data)
            client_socket.sendall(res)

        elif "register" in request_line:
            print("handle register request. {}".format(request_lines))
            proxy_type, remote_port, proxy_server = handle_register_request(
                request_data
            )
            proxy_port_map[remote_port] = {
                "remote_port": remote_port,
                "proxy_type": proxy_type,
                "proxy_server": proxy_server,
                "channel_socket": client_socket,
            }
            server_socket_list.append(proxy_server)
            proxy_socket_list.append(client_socket)

            read_socket_list.append(proxy_server)
            read_socket_list.append(client_socket)

        else:
            print("unkonown request, close socket. {}".format(request_lines))
            client_socket.close()

    except Exception as err:
        print(err)


def createNatServerSocket(ip, port):
    print("NatServer: '{}:{}', running...".format(ip, port))
    # await run_server(ip, port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    return server_socket


if __name__ == "__main__":

    nat_server = createNatServerSocket(ip="127.0.0.1", port=8080)
    server_socket_list.append(nat_server)
    read_socket_list.append(nat_server)

    while True:
        readable, writable, errored = select.select(read_socket_list, [], [])

        for s in readable:
            if s in server_socket_list:
                client_socket, address = s.accept()
                read_socket_list.append(client_socket)
                print("Connection from: {}".format(address))
            else:
                handle_request(s)

                if s not in proxy_socket_list:
                    read_socket_list.remove(s)
