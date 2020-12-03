import socket
import threading
import struct
import json
import os
def receive_file(c_id):
    try:
        #收報頭的長度
        obj = c_id.recv(4)
        header_size = struct.unpack('i', obj)[0]
        #收報頭
        header_bytes = c_id.recv(header_size)
        # 從報頭中解析出對真實資料的描述資訊
        header_json = header_bytes.decode('utf-8')
        header_dic = json.loads(header_json)
        # 文件传输
        path = os.path.join("sockettest", header_dic["deviceId"], header_dic["filename"])
        with open(path, "wb") as file:
            while True:
                # 接收数据
                file_data = c_id.recv(1024)
                # print(len(file_data), file_data)
                # 数据长度不为0写入文件
                if file_data:
                    file.write(file_data)
                    c_id.send("ok".encode('utf-8'))
                # 数据长度为0表示下载完成
                else:
                    break
    # 下载出现异常时捕获异常
    except Exception as e:
        with open('log.txt', "a") as f:
            f.writelines(str(e) + "\n")
            f.close()
        print("error", e)
    # 无异常则下载成功
    else:
        print("done")

if __name__ == '__main__':
    try:
        with open("socket_setting.json", "r", encoding="utf-8") as f:
            settingJson = json.load(f)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 获取本机名
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        server.bind((settingJson["sendIp"], settingJson["port"]))

        server.listen(5)
        print('start')

        while True:
            try:
                client_id, client_address = server.accept()
                # print()
                print(client_address, 'content')
                threading.Thread(target=receive_file, args=(client_id,)).start()
            except Exception as e:
                with open('log.txt', "a") as f:
                    f.writelines(str(e) + "\n")
                    f.close()
    except Exception as e:
        with open('log.txt', "a") as f:
            f.writelines(str(e) + "\n")
            f.close()
