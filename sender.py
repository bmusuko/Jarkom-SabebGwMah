import socket
import sys

host_address = sys.argv[1]
port = int(sys.argv[2])
file_path = []

i = 2

if (len(sys.argv) <= 3) : 
    sys.exit('Missing file argument!')

if (len(sys.argv) > 8) : 
    sys.exit('File argument is to much!')

while i < len(sys.argv) - 1 :
    i += 1
    file_path.append(sys.argv[i])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_address, port))
print("[+] Connected with Server")

# get file name to send
f_send = file_path[0]
# open file
with open(f_send, "rb") as f:
    # send file
    print("[+] Sending file...")
    data = f.read()
    # print(data)
    s.sendall(data)

    # close connection
    s.close()
    print("[-] Disconnected")
    sys.exit(0)