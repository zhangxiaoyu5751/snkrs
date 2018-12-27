import requests
import json
import config
import time


class AlertOver(object):

    def send_message(self, data, count=0):

            data = {
                "source": config.source_id,
                "receiver": config.receive_id,
                "content": json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False).encode('utf8'),
                "title": "snkrs发售通知"
            }
            try:
                res = requests.post(
                    "https://api.alertover.com/v1/alert",
                    data=data
                )
               
            except:
                time.sleep(3)
                count += 1
                if count < 20:
                    self.send_message(data, count)
                else:
                    pass
                    

if __name__ == '__main__':
    a = AlertOver()
    b = '啊'*21
    c = 'a'*39
    d = '啊'*100
    a.send_message(d)


