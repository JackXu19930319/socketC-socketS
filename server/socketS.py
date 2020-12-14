import socket
import threading
import struct
import os
import time
import configparser
def receive_file(c_id):
    try:
        # 第一步：先收報頭的長度
        obj = c_id.recv(4)
        c_id.send("ok".encode('utf-8'))
        header_size = struct.unpack('i', obj)[0]
        # 第二步：再收報頭
        header_bytes = c_id.recv(header_size)
        c_id.send("ok".encode('utf-8'))
        # 第三步：從報頭中解析出對真實資料的描述資訊
        header = header_bytes.decode('utf-8').split(",")
        # 文件传输
        if os.path.isdir("recData"):
            pass
        else:
            os.mkdir("recData")

        deviceId = header[0]
        if os.path.isdir(os.path.join("recData", deviceId)):
            pass
        else:
            os.mkdir(os.path.join("recData", deviceId))
        fileName = header[1]
        path = os.path.join("recData", deviceId, fileName)
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
        try:
            os.remove(path)
        except:
            pass
        with open('log.txt', "a") as f:
            f.writelines(str(e) + "\n")
            f.close()
        print("error", e)
    # 无异常则下载成功
    else:
        print("done")

if __name__ == '__main__':
    clients = []
    conf = configparser.ConfigParser()
    conf.read("setting.ini", encoding='utf-8')

    ip = conf.get('server', 'ip')
    port = int(conf.get('server', 'port'))
    rebot = True
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((ip, port))
    # server.setblocking(False)
    server.listen(5)
    print('start %s %s' % (ip, port))
    while rebot:
        try:
            rebot = False
            while True:
                try:
                    client_id, client_address = server.accept()
                    print(client_address, 'content')
                    threading.Thread(target=receive_file, args=(client_id,)).start()
                except Exception as e:
                    with open('log.txt', "a") as f:
                        f.writelines(str(e) + "\n")
                        f.close()
        except Exception as e:
            rebot = True
            with open('log.txt', "a") as f:
                f.writelines(str(time.ctime()) + ">>>" + str(e) + "\n")
                f.close()
        finally:
            time.sleep(1)