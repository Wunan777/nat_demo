# NAT demo. Usage:

## Prepare 
pip3 install requirements.txt

## NAT Server 
Run on NAT node.
```
python3 nat_server.py --port=8080
```
## NAT Client
Run on device which need NAT traversal.
```
NAT_SERVER="10.10.2.2:8080" python3 nat_client.py --type=http --local_port=8811 --remote_port=8811
```
remote {ip:port} <----> local {ip:port}

remote ip: nat server ip, example: `10.10.2.2 `  
remote port: args remote port  
local ip: local device ip, example: `127.0.0.1`  
local port: local port , example: `8811`  
type: protocol, example `http`