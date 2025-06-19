import gzip
import re
import hashlib
import requests
from websocket import WebSocketApp
import execjs
from ddd_pb2 import PushFrame, Response, ChatMessage, GiftMessage


def get_signature(s):
    # js逆向,获取signature值
    with open('sign.js', 'r') as f:
        js_code = f.read()

    signature = execjs.compile(js_code).call('get_signature', s)
    return signature


def on_open(ws):
    print("on_open", ws)


def on_message(ws, body):
    # body就是原始的文本

    # 1.转换PushFrame
    frame = PushFrame()
    frame.ParseFromString(body)

    # 2.根据Response+gzip解压数据,生成数据对
    origin_bytes = gzip.decompress(frame.payload)
    response = Response()
    response.ParseFromString(origin_bytes)

    # if response.needAck:
    if response.need_ack:
        s = PushFrame()
        s.payload_type = 'ack'
        s.payload = response.internal_ext.encode('utf-8')
        s.LogID = frame.LogID
        ws.send(s.SerializeToString())

    # 3.读取所有的数据
    for item in response.messages:
        # 礼物信息
        if item.method == 'WebcastGiftMessage':
            message = GiftMessage()
            message.ParseFromString(item.payload)
            # 处理逻辑,处理逻辑可能有一点小问题,需要调整一下
            user_id = message.user.id
            group_id = str(message.group_id)
            gift_id = message.gift.id
            current_count = message.total_count

            key = (user_id, gift_id, group_id)
            last_count = handled_gift_groups.get(key, 0)
            delta = current_count - last_count
            if delta <= 0:
                return
            handled_gift_groups[key] = current_count
            print(f'【礼物】group_id:{message.group_id},礼物ID:{message.gift.id},用户名:{message.user.nickName},礼物名称:{message.gift.name},礼物价值:{message.gift.diamond_count},total_count:{message.total_count}')

        # 聊天信息
        if item.method == 'WebcastChatMessage':
            message = ChatMessage()
            message.ParseFromString(item.payload)
            info = f"【弹幕】{message.user.nickName}:{message.content},抖音账号:{message.user.shotId}"
            print(info)


def on_error(ws, message):
    print("on_open", ws, message)


def on_close(ws, *args, **kwargs):
    pass


def fetch_live_room_info(web_url):
    res = requests.get(url=web_url, headers=headers, cookies=cookies)

    # 1.获取room_id,up(博主昵称)
    match_list = re.findall(r'"roomId\\":\\"(\d+)\\",', res.text)
    match_list1 = re.findall(r'"nickname\\":\\"(.*?)\\"', res.text)
    room_id = match_list[0]
    up = match_list1[-1]
    # print(room_id,up)

    # 2.构造固定的字符串
    o = f'live_id=1,aid=6383,version_code=180800,webcast_sdk_version=1.0.14-beta.0,room_id={room_id},sub_room_id=,sub_channel_id=,did_rule=3,user_unique_id=7359170990646314547,device_platform=web,device_type=,ac=,identity=audience'

    # 3.进行md5加密
    stub = hashlib.md5(o.encode('utf-8')).hexdigest()
    # print(stub)

    # 4.js逆向,调用函数,传入stub值,获取signature
    signature = get_signature(stub)
    # print(signature)
    # 5.拼接得到wss地址
    wss_url = f'wss://webcast5-ws-web-hl.douyin.com/webcast/im/push/v2/?app_name=douyin_web&version_code=180800&webcast_sdk_version=1.0.14-beta.0&update_version_code=1.0.14-beta.0&compress=gzip&device_platform=web&cookie_enabled=true&screen_width=1707&screen_height=960&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/129.0.0.0%20Safari/537.36&browser_online=true&tz_name=Asia/Shanghai&cursor=d-1_u-1_h-7415969050658034722_t-1726664969296_r-1&internal_ext=internal_src:dim|wss_push_room_id:{room_id}|wss_push_did:7359170990646314547|first_req_ms:1726664969175|fetch_time:1726664969296|seq:1|wss_info:0-1726664969296-0-0|wrds_v:7415969568708889208&host=https://live.douyin.com&aid=6383&live_id=1&did_rule=3&endpoint=live_pc&support_wrds=1&user_unique_id=7359170990646314547&im_path=/webcast/im/fetch/&identity=audience&need_persist_msg_count=15&insert_task_id=&live_reason=&room_id={room_id}&heartbeatDuration=0&signature={signature}'

    ttwid = res.cookies.get_dict()['ttwid']  # 下一步请求所需参数
    return room_id, up, wss_url, ttwid


def run():
    # 直播间链接
    # 341619001773
    web_url = 'https://live.douyin.com/158922641497'
    room_id, up, wss_url, ttwid = fetch_live_room_info(web_url)
    print(f'欢迎来到{up}的直播间,房间ID:{room_id}')
    print('开始建立连接中...')
    ws = WebSocketApp(
        url=wss_url,
        header=headers,
        cookie=f"ttwid={ttwid}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()


if __name__ == '__main__':
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    cookies = {
        "__ac_nonce": "06723018d00888333ca5b"
    }
    handled_gift_groups = {}
    run()
