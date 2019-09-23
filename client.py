import socket
import sys
import random
import time

CHUNK_SIZE = 32 * 1024
TYPE_DATA = 0x0
TYPE_ACK = 0x1
TYPE_FIN = 0x2
TYPE_FIN_ACK = 0x3

def intToByteObject16Bits(value):
    x = value
    y = 0
    if (x >= 256):
        y = x >> 8
        x = x % 256
    return bytes([y]) + bytes([x])

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

file_id = random.randrange(0,16,1)

# open file
with open(f_send, "rb") as f:
    type_and_id = (TYPE_DATA << 4) + file_id        #Type and ID
    sequence_number = 0                             #Sequence Number
    # send file
    print("[+] Sending file...")
    chunk = f.read(CHUNK_SIZE)
    while chunk:
        packet = bytes([type_and_id])
        packet += intToByteObject16Bits(sequence_number)
        packet += intToByteObject16Bits(len(chunk))
        packet += intToByteObject16Bits(12345)           #CHECKSUM BELOM KELAR
        packet += chunk
        s.send(packet)
        time.sleep(0.5)
        print("Packet "+str(sequence_number)+" has been sent to "+host_address)
        chunk = f.read(CHUNK_SIZE)
        print(len(chunk))
        if (len(chunk) < 32 * 1024):
            type_and_id = (TYPE_FIN << 4) + file_id
        sequence_number += 1
    
    # close connection
    s.close()
    print("[-] Disconnected")
    sys.exit(0)