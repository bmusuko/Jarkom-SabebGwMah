import socket
import sys
import random
import time
import os

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

def checksum(x):
	n = len(x)
	if n%2 == 1:
		x += bytes([0])
		n +=1
	s = 0
	t = n // 2
	for i in range (t):
		y = 2*i
		s ^= (x[y]<<8 + x[y+1])
	return s%65536

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
s.settimeout(1)

print("[+] Connected with Server")

# get file name to send

f = [None, None, None, None, None]
done = [False, False, False, False, False]
chunk = [None, None, None, None, None]
seq_num = []
fin_counter = 0

for x in range (len(file_path)):
    # open file
    f_send = file_path[x]
    f[x] = open(f_send, "rb")
    seq_num.append(0)

while True:
    for i in range(len(file_path)):
        if (not done[i]):
            print()
            print("Ini file ke-"+str(i))
            file_id = i
            sequence_number = seq_num[i]

            # send file
            print("[+] Sending file...")

            if (not chunk[i]):
                 chunk[i] = f[i].read(CHUNK_SIZE)

            if (len(chunk[i]) < (32 * 1024)):
                type_and_id = (TYPE_FIN << 4) + file_id
            else:
                type_and_id = (TYPE_DATA << 4) + file_id

            print("INI SIZE PACKET KE "+str(sequence_number)+" : "+str(len(chunk[i])))

            packet = None
            packet = bytes([type_and_id])
            packet += intToByteObject16Bits(sequence_number)
            packet += intToByteObject16Bits(len(chunk[i]))
            # print("INI HEADER :"+ str(packet))
            packet += intToByteObject16Bits(checksum(packet+chunk[i]))
            packet += chunk[i]

            if(type_and_id>>4 == 0x2):
                extension = os.path.splitext(f_send)[1]
                packet += extension.encode()

            print("INI TYPENYA "+str(type_and_id >> 4))
            s.send(packet)
            ack = s.recv(1)
            print("Packet "+str(sequence_number)+" has been sent to "+host_address)
            print ("INI ACKNYA : "+str(ack))

            if (ack == b'\x01'):
                print("Ack has been received")
                seq_num[i] += 1
                chunk[i] = None
            elif (ack == b'\x03'):
                chunk[i] = None
                print("Final ack has been received")
                done[i] = True
                fin_counter += 1
                f[i].close()

            if (done[i]):
                break

    if (fin_counter == len(file_path)):
        break

# close connection
s.close()
print("[-] Disconnected")
sys.exit(0)