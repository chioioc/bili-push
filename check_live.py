import requests
import os

# 配置信息
ROOM_ID = os.environ['ROOM_ID']
BARK_KEY = os.environ['BARK_KEY']
STATUS_FILE = "status.txt"

def get_live_status():
    url = f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={ROOM_ID}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers).json()
        info = res['data']['room_info']
        return info['live_status'], info['title']
    except:
        return 0, ""

def main():
    current_status, title = get_live_status()
    
    # 读取上一次的状态
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            last_status = f.read().strip()
    else:
        last_status = "0"

    # 如果从 0 (未开播) 变成 1 (开播)
    if current_status == 1 and last_status == "0":
        print("检测到开播，发送推送...")
        push_url = f"https://api.day.app/{BARK_KEY}/主播开播啦/{title}?url=bilibili://live/{ROOM_ID}&group=Bili"
        requests.get(push_url)
    
    # 更新状态文件
    with open(STATUS_FILE, "w") as f:
        f.write(str(current_status))

if __name__ == "__main__":
    main()
