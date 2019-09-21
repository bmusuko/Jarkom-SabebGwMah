import socket
import sys



HOST = "192.168.88.7"
if(len(sys.argv)<2):
    sys.exit("argument not sufficient")
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print("Listening ...")
while True:
    conn, addr = s.accept()
    print("[+] Client connected: ", addr)
    #print(data.strip(),addr)
    #print(repr(data))

    # get file name to download
    f = open("data_received", "wb")
    while True:
        # get file bytes
        data = conn.recv(3276800)
        if not data:
            break
        # write bytes on file
        f.write(data)
    f.close()
    print("[+] Download complete!")

    # close connection
    conn.close()
    print("[-] Client disconnected")
    sys.exit(0)