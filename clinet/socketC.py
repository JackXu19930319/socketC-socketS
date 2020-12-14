# coding=utf-8
import struct
import socket
import time
import sys

class socketClient():
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect((ip, port))

    def sendObj(self, file_path, head):
        # 先發送報頭的長度
        self.client.send(struct.pack('i', len(head)))
        if self.client.recv(1024).decode('utf-8') == 'ok':
            pass
        else:
            print("error")
            return False
        # 再發報頭
        self.client.send(head.encode('utf-8'))
        if self.client.recv(1024).decode('utf-8') == 'ok':
            pass
        else:
            print("error")
            return False
        # 最後發資料
        try:
            with open(file_path, "rb") as file:
                while True:
                    file_data = file.read(1024)
                    if file_data:
                        self.client.send(file_data)

                        if self.client.recv(1024).decode('utf-8') == 'ok':

                            pass
                        else:
                            print("error")
                            return False
                    else:
                        return True
        except Exception as e:
            with open('log.txt', "a") as f:
                f.writelines("Class socketClient : " + str(e) + "\n")
                f.close()
            print("Class socketClient : " + str(e))
        finally:
            self.client.close()

if __name__ == '__main__':
    # python socketC.py 127.0.0.1 8000 /Users/jx/Desktop/專案名稱.jpg 1 LM-01,test.jpg
    # socketC.exe 127.0.0.1 8000 /Users/jx/Desktop/專案名稱.jpg 1 LM-01,test.jpg
    inputData = sys.argv
    ip = str(inputData[1])
    port = int(inputData[2])
    filePath = str(inputData[3])

    if len(inputData) > 4:
        isReSend = str(inputData[4])

    if len(inputData) > 5:
        head = str(inputData[5])
    else:
        head = ""

    print("ip: %s, port: %s, file: %s, header: %s" %(ip, port, filePath, head))

    reCount = 5
    count = 0
    ####################################
    if filePath.find("\\") != -1:
        filePath = filePath.replace("\\", "/")
    fileName = filePath.split("/")[-1]
    isSend = True
    while isSend:
        try:
            client = socketClient(ip, port)
            if client.sendObj(filePath, head):
                isSend = False
                count = 0
                print("%s >> done" %(fileName))
        except Exception as e:
            count += 1
            print("main : " + str(e))
            if count > reCount:
                with open('log.txt', "a") as f:
                    f.writelines("main : " + str(e) + "\n")
                    f.close()
                time.sleep(1)
                count = 0
                if isReSend == "1":
                    isSend = True
                else:
                    isSend = False
        ####################################
