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
    with open("socket_setting.json", "r", encoding="utf-8") as f:
        settingJson = json.load(f)

    filePath = settingJson["filePath"]

    files = os.listdir(filePath)

    count = 0
    reCount = settingJson["reCount"]
    port = settingJson["port"]
    ip = settingJson["sendIp"]
    ####################################
    for f in files:
        fileName = str(i) + "_" + str(f)
        heardDict = {
            "filename": fileName,
            "deviceId": settingJson["deviceId"]
        }
        isSend = True
        while isSend:
            try:
                client = socketClient(ip, port)
                if client.sendObj(os.path.join(filePath, f), heardDict):
                    isSend = False
                    count = 0
                    print("%s >> done" %(fileName))
            except Exception as e:
                count += 1
                print("ERROR: %s>>%s" % (os.path.join(filePath, f), e))
                if count > reCount:
                    with open('log.txt', "a") as f:
                        f.writelines(str(e) + "\n")
                        f.close()
                    time.sleep(20)
                count = 0
                isSend = True
                pass
        ####################################
