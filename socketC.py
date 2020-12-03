# coding=utf-8
import struct
import os
import socket
import json
import time

class socketClient():
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))
        # print('connect successful')

    def sendObj(self, file_path, heardDict={}):
        header_json = json.dumps(heardDict)
        header_bytes = header_json.encode('utf-8')
        # 先發送報頭的長度
        self.client.send(struct.pack('i', len(header_bytes)))
        # 再發報頭
        self.client.send(header_bytes)
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
                f.writelines(str(e) + "\n")
                f.close()
            print(e)
        finally:
            self.client.close()

if __name__ == '__main__':
    fuleFullPath = "data.txt"
    heardDict = {
    "fileName" : "data.txt",
    }
    reSend = False
    while reSend:
        try:
            if count < reCount:
                client = socketClient("127.0.0.1", 8000)
                if client.sendObj(fuleFullPath, heardDict):
                    reSend = False
                    count = 0
                    print("%s >> done" %(f))
            else:
                reSend = False
        except Exception as e:
            count += 1
            print("ERROR: %s>>%s" % (os.path.join(filePath, f), e))
            with open('log.txt', "a") as f:
                f.writelines(str(e) + "\n")
                f.close()
            pass
