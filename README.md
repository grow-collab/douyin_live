项目结构:
  dy_live.py -> 1.主文件,构建wss链接(获取room_id,signature),接收响应消息，用我们已知的protobuf格式,解析数据,处理弹幕和礼物数据
  room_id.py -> 2.通过直播间链接,获取房间ID
  sign.js    -> 3.js逆向，用于获取wss链接中signature的值(传值,用算法模拟加密)
             ->对于wss链接中signature的获取，除了js逆向,还可以使用RPC远程调用。
  ddd_pd2.py -> 4.用于解析数据的protubuf文件(通过已知的protobuf格式,转换过来的)
  ddd.proto  -> 用于解析抖音服务器发送给我们消息的protobuf数据格式
