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


def handle_create_proxy_request(data: bytes):
    # example: 'http;8811'
    proxy_type, remote_port = data.decode().split(";")
    if proxy_type == "http":
        port = remote_port
        proxy_server = createHttpProxySocket(ip="127.0.0.1", port=port)
        return proxy_type, remote_port, proxy_server
    else:
        raise Exception("unvalid proxy_type : {}".format(proxy_type))


def handle_request(client_socket):
    request_data = client_socket.recv(1024)
    if not request_data:
        print("client socket close, {}".format(client_socket))
        client_socket.close()

    # 解析HTTP请求头
    headers = request_data.decode().split("\r\n")
    if headers:
        request_line = headers[0]
        method, path, protocol = request_line.split(" ")
        print(method, path, protocol)

    else:
        proxy_type, remote_port, proxy_server = handle_create_proxy_request(
            request_data
        )
        proxy_port_map[remote_port] = {
            "remote_port": remote_port,
            "proxy_type": proxy_type,
            "proxy_server": proxy_server,
            "channel_socket": client_socket,
        }
        proxy_socket_list.append(client_socket)

    # client_socket.close()


def createNatServerSocket(ip, port):
    print("NatServer: '{}:{}', running...".format(ip, port))
    # await run_server(ip, port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    return server_socket


if __name__ == "__main__":

    nat_server = createNatServerSocket(ip="127.0.0.1", port=8080)
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
