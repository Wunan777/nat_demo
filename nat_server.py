import socket
import select
import argparse
from src.const import RECV_MAX_SIZE

# In NAT Server, will exist 3 type socket,
#  - `server socket`,
#  - `conn socket`(created by actively connecting nat server)
#  - `http socket`(created by http request, which will be closed after http response)
# Caution: The `server socket` and `conn socket` need to be persistent.
server_socket_list = []
conn_socket_list = []
http_socket_list = []

# The socket which `server socket` created directly or  indirectly, should put into the `read socket` list.

proxy_nat_client_port_map = {}


def createNatServerSocket(ip, port):
    print("NatServer: '{}:{}', running...".format(ip, port))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    return server_socket


def createRemoteHttpSocket(ip, port):
    print("RemoteHttp: '{}:{}', running...".format(ip, port))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    return server_socket


def handle_register_request(data: bytes):
    message = data.decode()
    print("handle register request data: {}".format(message))
    if not message:
        raise Exception("handle_register_request err: no data")

    flag_filed, proxy_type, remote_port = message.split(";")
    if proxy_type == "http":
        port = int(remote_port)
        server_socket = createRemoteHttpSocket(ip="0.0.0.0", port=port)
        return proxy_type, remote_port, server_socket
    else:
        raise Exception("unvalid proxy_type : {}".format(proxy_type))


def find_proxy_nat_client(register_port):
    if register_port not in proxy_nat_client_port_map:
        return None
    else:
        return proxy_nat_client_port_map[register_port]["channel_socket"]


def find_request_host(request_lines):
    request_port = None
    for request_line in request_lines:
        if "host" in request_line.lower():
            request_port = request_line.split(":")[-1]

    if not request_port:
        raise Exception(
            "according request_data, request_port not found. Detail: {}".format(
                request_lines
            )
        )
    return request_port


def handle_http_request_proxy_to_nat_client(req_port, req_data):
    # s = proxy_nat_client_port_map[req_port]["channel_socket"]
    proxy_nat_client_socket = find_proxy_nat_client(req_port)
    if not proxy_nat_client_socket:
        errmsg = "Req port: {}, not register.".format(req_port)
        raise Exception(errmsg)

    else:
        proxy_nat_client_socket.sendall(req_data)
        recv_data = proxy_nat_client_socket.recv(RECV_MAX_SIZE)
        return recv_data


def handle_http_request(s, request_data):
    # [
    #     "GET / HTTP/1.1",
    #     "Host: 127.0.0.1:8812",
    #     "Connection: keep-alive",
    #     "Cache-Control: max-age=0",
    # ]
    request_lines = request_data.decode().split("\r\n")
    print("handle http request. {}".format(request_lines))
    header = request_lines[0]
    host_info = request_lines[1]

    method, path, protocol = header.split(" ")
    print(method, path, protocol)

    request_port = find_request_host(request_lines)
    res = handle_http_request_proxy_to_nat_client(request_port, request_data)
    print("recv handle_http_request res: {}".format(res))
    s.sendall(res)


def handle_request(s):
    request_data = s.recv(RECV_MAX_SIZE)
    if not request_data:
        print("Due to no data reva, client socket close, {}".format(s))
        s.close()

    # request_data expect 3 type.
    #   -  http request data
    #   -  cmd: request `nat server` bind ip
    #   -  other.
    try:

        request_lines = request_data.decode().split("\r\n")
        request_line = request_lines[0]

        if "HTTP" in request_line:
            # Parse HTTP header
            # ---------------
            # HTTP/1.1 200 OK
            # Server: nginx
            # Content-Type: text/html
            # Content-Length: 12
            handle_http_request(s, request_data)
            # if s in http_socket_list:
            #     http_socket_list.remove(s)
            print("http socket handled, should be removed, {}".format(s))
            s.close()

        elif "register" in request_line:
            # Parse register command header
            # ---------------
            # example: 'register;http;8811'
            proxy_type, remote_port, server_socket = handle_register_request(
                request_data
            )
            proxy_nat_client_port_map[remote_port] = {
                "remote_port": remote_port,
                "proxy_type": proxy_type,
                "server_socket": server_socket,
                "channel_socket": s,
            }
            server_socket_list.append(server_socket)

        else:
            print("unkonown request, close socket. {}".format(request_data))
            s.close()

    except Exception as err:
        print(err)


def main():
    parser = argparse.ArgumentParser(description="NAT Client")
    parser.add_argument("--port", help="Nat Server Port.", required=True)
    args = parser.parse_args()

    nat_server_socket = createNatServerSocket(ip="0.0.0.0", port=int(args.port))
    server_socket_list.append(nat_server_socket)
    try:

        while True:
            # fileno: -1 , closed.
            read_socket_list = [
                s
                for s in (server_socket_list + conn_socket_list + http_socket_list)
                if s.fileno() != -1
            ]

            readable, writable, errored = select.select(read_socket_list, [], [])

            for s in readable:
                if s in server_socket_list:
                    # For server socket (which bind port to watch request), it create socket.
                    conn_socket, address = s.accept()
                    conn_socket_list.append(conn_socket)
                    print("Connection from: {}".format(address))
                else:
                    # For the other socket, handle the data from socket recv.
                    handle_request(s)

    except Exception as err:
        print(err)

    finally:
        nat_server_socket.close()


if __name__ == "__main__":
    main()
