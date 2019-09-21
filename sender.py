import socket
import sys

host_address = sys.argv[1]
port = sys.argv[2]
file_address = []

i = 2

if (len(sys.argv) <= 3) : 
    sys.exit('Missing file argument!')

if (len(sys.argv) > 8) : 
    sys.exit('File argument is to much!')

while i < len(sys.argv) - 1 :
    i += 1
    file_address.append(sys.argv[i])

# UDP_IP = "127.0.0.1"
# UDP_PORT = 8000
# MESSAGE = "Hello, World!"

# print "UDP target IP:", UDP_IP
# print "UDP target port:", UDP_PORT
# print "message:", MESSAGE

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))