 
import socket
import sys
import time
import threading

files =[b'',b'',b'',b'',b'']
counter_sequence_number = [0,0,0,0,0]

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

HOST = "192.168.43.32"
if(len(sys.argv)<2):
    sys.exit("argument not sufficient")
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Listening ...")

client_socket, addr = s.accept()
print("[+] Client connected: ", addr)
while True:
    request =None
    request = client_socket.recv(32999)
    if request == b'':
        print("packet kosong")
        client_socket.close()
        print("[-] Client disconnected")
        sys.exit(0)

    type_packet = (request[0] >> 4)%16
    id_packet = request[0] % 16
    sequence_number = (request[1] << 8) + request[2] 
    length = (request[3] << 8) + request[4]
    checksums = (request[5] << 8) + request[6]
    if ((checksums) == checksum (request[0:5]+(request[7:length+7]))):
        if(sequence_number==counter_sequence_number[id_packet]): 
            print("[+] Packet - "+str(sequence_number+1)+" Received")
            print("type packet : "+str(type_packet))
            print("id packet : "+ str(id_packet))
            print("sequence_number : " +str(sequence_number+1))
            print("length : " +str(length))
            print("checksum : "+str(checksums))
            files[id_packet] += request[7:length+7]

            if(type_packet == 0x2):
                #print(request[(length+7):(length+7)+4])
                extension = request[(length+7):(length+11)].decode()
                counter_sequence_number[id_packet] += 1
                f = open("output_"+str(id_packet)+extension, "wb")
                print(id_packet)
                print("FIN ACK")
                f.write(files[id_packet])
                f.close()
                client_socket.send(b'\x03')
            elif(type_packet == 0x00):
                counter_sequence_number[id_packet] += 1
                print("ACK BIASA")
                client_socket.send(b'\x01')
            else:
                print("UNIDENTIFIED")
    else:
        print("checksum salah")

