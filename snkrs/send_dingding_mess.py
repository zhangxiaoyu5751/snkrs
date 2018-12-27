# -*- coding: utf-8 -*-
import requests
import json

def send_message():
    url = 'https://oapi.dingtalk.com/robot/send?access_token=46d4b028bcab569415bd06e2b8c412c9690aae2e5556f3adff63b810c2f3d392'
    header = {'Content-Type': 'application/json'}
    data = {
     "msgtype": "markdown",
     "markdown": {"title":"杭州天气",
     "text":"#### 杭州天气  \n >  西北风1级，空气良89，相对温度73%\n\n > ![screenshot](http://i01.lw.aliimg.com/media/lALPBbCc1ZhJGIvNAkzNBLA_1200_588.png)\n  > ###### 10点20分发布 [天气](http://www.thinkpage.cn/) "
     },
    "at": {
        "atMobiles": [
            "18800144312"
        ], 
        "isAtAll": True
    }
    }
    response = requests.post(url, headers=header, data=json.dumps(data))
    print(response)
    return True

if __name__ == '__main__':
    send_message()
