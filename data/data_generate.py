import csv
import time

import requests
import json

# 修改成自己的api key和secret key
API_KEY = "YEXtjjnQvZMmMnaCYsPjYGA2"
SECRET_KEY = "yqWImNmkbo1N8wSYaqquAUdiwuNDquZc"


def main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()
    poets = open('poets.txt', encoding='utf-8')
    poets_csv = open('poets.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(poets_csv)

    for poet in poets.readlines():
        print(poet.strip('\n'))
        s = "请按照年份介绍一下{}的生平，不要序号，每行包含年份和当年发生的事件".format(poet.strip('\n'))
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": s
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload).json()

        print(res['result'])
        writer.writerow(["请介绍一下{}的生平".format(poet.strip('\n')), res['result']])
        # time.sleep(10)




def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+API_KEY+"&client_secret="+SECRET_KEY
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json().get("access_token"))
    return response.json().get("access_token")


if __name__ == '__main__':

    main()