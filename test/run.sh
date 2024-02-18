# Test socket.
PYTHONPATH=$PYTHONPATH:${BASE_DIR} python3 socket_server.py
PYTHONPATH=$PYTHONPATH:${BASE_DIR} python3 socket_client.py

PYTHONPATH=$PYTHONPATH:/Users/nanwu/Documents/GitHub/nat_demo  python3 socket_server.py

# Test NAT Server 
# case1: register , then request.
# case2: no register, then request.