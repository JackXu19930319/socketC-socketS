# socketC-socketS
'''python
  header_json = json.dumps(heardDict)
  header_bytes = header_json.encode('utf-8')
  # 先發送報頭的長度
  self.client.send(struct.pack('i', len(header_bytes)))
  # 再發報頭
  self.client.send(header_bytes)
