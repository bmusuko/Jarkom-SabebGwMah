import socket
import sys
import time
import threading

file = b''
counter_file = 0
counter_sequence_number = -1



HOST = "192.168.43.32"
if(len(sys.argv)<2):
    sys.exit("argument not sufficient")
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Listening ...")
while True:
    print("tete")
    client_socket, addr = s.accept()
    print("[+] Client connected: ", addr)
    while True:
        request = client_socket.recv(32775)
        if request == b'':
            print("1")
            client_socket.close()
            break
        type_packet = request[0] >> 4
        id_packet = request[0] % 16
        sequence_number = (request[1] << 8) + request[2]
        length = (request[3] << 8) + request[4]
        checksum = (request[5] << 8) + request[6]
        file += request[7:]
        counter_sequence_number += 1
        print("type packet : "+str(type_packet))
        print("id packet : "+ str(id_packet))
        print("sequence_number : " +str(sequence_number))
        print("length : " +str(length))
        print("checksum : "+str(checksum))
        if(type_packet == 0x2):
            f = open("output_"+str(id_packet)+".jpg", "wb")
            print("2")
            f.write(file)
            f.close()
            file = b''
            client_socket.send(b'\x03')
            print("[-] Client disconnected")
            sys.exit(0)
        elif(type_packet == 0x00):
            print("3")
            client_socket.send(b'\x01')
        else:
            print("4")
            client_socket.send(b'\xff')
        client_socket.close()
        break

sys.exit(0)
print("[-] Client disconnected")