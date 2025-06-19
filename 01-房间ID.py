import re
import requests

# 获取room_id(直播间id)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
cookies = {
    "UIFID_TEMP": "fd93a02f3f52f94d15e514b5060909b7718dbdccf5e652d020e98a2368c5c67f9c0d737848b4ca649635da2ed74acc44ef43447979efbb873a1cae98abb6e0c92b4abdd3c686f33b8b6a0041f5bcb0ac",
    "hevc_supported": "true",
    "UIFID": "fd93a02f3f52f94d15e514b5060909b7718dbdccf5e652d020e98a2368c5c67f9c0d737848b4ca649635da2ed74acc4470ec17ae24ef211a0ed2dcd83e61b2febc6b9a2d24d884d897fcef6188287e51f910dec2580cf1fac82c8ff304c365065df03343b5590229644fe1b59fdf861a9e0d7db4786183c3dc181470b5339729f05ad2dfe7841e7f4f6ff4a13ea83c45bbffb70dcdaf26f685bfe6d062fc61ba",
    "xgplayer_device_id": "73968815451",
    "xgplayer_user_id": "987173763174",
    "live_use_vvc": "%22false%22",
    "fpk1": "U2FsdGVkX1/NfnNxlP9vFeYV4mxBAu+tstqhb4gt1zOH8Z92lf6aydpKb0z4EB8TAdPIv4E4crRDNKnFAs+Y0A==",
    "fpk2": "33d0f257a817d1ca4c4381b87f8ad83f",
    "__live_version__": "%221.1.3.3838%22",
    "FORCE_LOGIN": "%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D",
    "passport_csrf_token": "d42a655a416054b312a6b1408910480d",
    "passport_csrf_token_default": "d42a655a416054b312a6b1408910480d",
    "__security_mc_1_s_sdk_crypt_sdk": "c95807fe-45c1-9241",
    "bd_ticket_guard_client_web_domain": "2",
    "enter_pc_once": "1",
    "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22",
    "strategyABtestKey": "%221749771155.27%22",
    "ttwid": "1%7C22O9F26ZH-e3QTBY0SQMV9c48jNPAOAN0l1Putvp_eE%7C1749771154%7C1c4254acf65ce0fca18c19863a08e7612e7a72de655cbf288f16ce990e80a2b9",
    "download_guide": "%221%2F20250613%2F0%22",
    "passport_mfa_token": "CjW8scGrWmsDo9UVjsOj7s4TMMh%2Bn7mF5qM8M36nq%2F10DPyUBNFz5slA4LnpWS4MbNwyiMVGyBpKCjwAAAAAAAAAAAAATxvAY6moaey3Jd95QiMUJDgGcHNbXe%2BEzyYSmN2TMJiDk4UmXKAqNiN2g285DXByJasQ3PnzDRj2sdFsIAIiAQMRt1lM",
    "d_ticket": "f6330b44660525b397a67b56c52ab51f70bf2",
    "passport_assist_user": "Cjzk4UQPVcr8R9_OiEHNTtT1JJPxk7NvANwMpi0_CYKxNnQcmJSbGt9_-HiHd-fMRkg40ov5jKyfMZHHs9AaSgo8AAAAAAAAAAAAAE8bCblaR_3-pjcyPZuGw3hn4hc8o6yMqWE45fg2DiA_BNgCDMgIkpBC-8X-yj7nRRPnEPr48w0Yia_WVCABIgEDpZkqSQ%3D%3D",
    "n_mh": "TrsM6_icDGPud-5VoXu1FUiksrHIUfNbE92eMELADC4",
    "sid_guard": "086b4c18281ca1769f9ff32edae8d57d%7C1749771234%7C5184000%7CMon%2C+11-Aug-2025+23%3A33%3A54+GMT",
    "uid_tt": "a41a1372a4da95ed95984f16e4ca151e",
    "uid_tt_ss": "a41a1372a4da95ed95984f16e4ca151e",
    "sid_tt": "086b4c18281ca1769f9ff32edae8d57d",
    "sessionid": "086b4c18281ca1769f9ff32edae8d57d",
    "sessionid_ss": "086b4c18281ca1769f9ff32edae8d57d",
    "is_staff_user": "false",
    "sid_ucp_v1": "1.0.0-KDJkNzE0MDc5MWNhZjlhMDE4YjU3MjQyMDkxMDQ3NTRkNTg5N2E0ZGMKHwje3c-otwIQ4setwgYY7zEgDDCOk53SBTgHQPQHSAQaAmxmIiAwODZiNGMxODI4MWNhMTc2OWY5ZmYzMmVkYWU4ZDU3ZA",
    "ssid_ucp_v1": "1.0.0-KDJkNzE0MDc5MWNhZjlhMDE4YjU3MjQyMDkxMDQ3NTRkNTg5N2E0ZGMKHwje3c-otwIQ4setwgYY7zEgDDCOk53SBTgHQPQHSAQaAmxmIiAwODZiNGMxODI4MWNhMTc2OWY5ZmYzMmVkYWU4ZDU3ZA",
    "login_time": "1749771235651",
    "is_dash_user": "1",
    "volume_info": "%7B%22volume%22%3A0.6%7D",
    "DiscoverFeedExposedAd": "%7B%7D",
    "SelfTabRedDotControl": "%5B%5D",
    "_bd_ticket_crypt_cookie": "5e666c007c243fefd50d33eb7a3ccd29",
    "__security_mc_1_s_sdk_sign_data_key_web_protect": "8d210735-4b54-b940",
    "__security_mc_1_s_sdk_cert_key": "46b57b1e-4c2d-859e",
    "__security_server_data_status": "1",
    "publish_badge_show_info": "%221%2C0%2C0%2C1749771245101%22",
    "h265ErrorNumNew": "-1",
    "WallpaperGuide": "%7B%22showTime%22%3A0%2C%22closeTime%22%3A0%2C%22showCount%22%3A0%2C%22cursor1%22%3A0%2C%22cursor2%22%3A0%7D",
    "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAAZmqQlkPJhCB0qRKO8vdDtdwb8m6TCpiQZJtBpvOUHD8%2F1749830400000%2F1749771242056%2F0%2F1749788848009%22",
    "__druidClientInfo": "JTdCJTIyY2xpZW50V2lkdGglMjIlM0ExMzY2JTJDJTIyY2xpZW50SGVpZ2h0JTIyJTNBMzk0JTJDJTIyd2lkdGglMjIlM0ExMzY2JTJDJTIyaGVpZ2h0JTIyJTNBMzk0JTJDJTIyZGV2aWNlUGl4ZWxSYXRpbyUyMiUzQTEuMjUlMkMlMjJ1c2VyQWdlbnQlMjIlM0ElMjJNb3ppbGxhJTJGNS4wJTIwKFdpbmRvd3MlMjBOVCUyMDEwLjAlM0IlMjBXaW42NCUzQiUyMHg2NCklMjBBcHBsZVdlYktpdCUyRjUzNy4zNiUyMChLSFRNTCUyQyUyMGxpa2UlMjBHZWNrbyklMjBDaHJvbWUlMkYxMzcuMC4wLjAlMjBTYWZhcmklMkY1MzcuMzYlMjIlN0Q=",
    "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAAZmqQlkPJhCB0qRKO8vdDtdwb8m6TCpiQZJtBpvOUHD8%2F1749830400000%2F1749788255685%2F1749788248009%2F0%22",
    "home_can_add_dy_2_desktop": "%221%22",
    "__ac_nonce": "0684badb700296809a40f",
    "__ac_signature": "_02B4Z6wo00f01gDTyBAAAIDDsh5TWCB1nz4A88yAAOiN8b",
    "has_avx2": "null",
    "device_web_cpu_core": "12",
    "device_web_memory_size": "8",
    "csrf_session_id": "03d74946f3734fcf4988526d453643fc",
    "odin_tt": "a1ed1d63c2ff377e886dee4b0ed9d6b699b5e0f7d840166703cf96d29b7fad7382508635ea6fa626a13baf2e4e86265c4d3c0f287a519ef7c84c711fb182c1dc",
    "xg_device_score": "6.965734300177489",
    "live_can_add_dy_2_desktop": "%220%22",
    "IsDouyinActive": "true",
    "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTGRmWkJuR3ZTcmlsaWxnOW9WWFZkSFNEbmFsKzlyVmJBejBRZTdiamI2ZnZKOUYxcExEcEdKVUUzeEpQUTFYckxoNlQ4RGhBYjVVOG5LMlRCSGRwWmc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
    "passport_fe_beating_status": "true",
    "webcast_local_quality": "origin"
}
url = "https://live.douyin.com/326624872646"
response = requests.get(url, headers=headers, cookies=cookies)

match_list = re.findall(r'"roomId\\":\\"(\d+)\\",', response.text)
room_id = match_list[0]
print(room_id)
