import time
import socket
import base64

ipadd = "127.0.0.1"
port = 6634
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ipadd, port))
s.listen(5)

print("Waiting for client... \n")

file=open(f'recived_files\\zipped.zip','wb+')
#Print Client Data
while True:
    try:
        conn, addr = s.accept()
        print("Connected by " + str(addr) + "\n")
        try:
            while True:
                zipped_file = conn.recv(1024)
                while(zipped_file):
                    file.write(zipped_file)
                    zipped_file=conn.recv(1024)
                quit()
        except Exception as E:
                print(E)
                break
    finally:
        print("\n connection is closed... ")
    conn.close()

