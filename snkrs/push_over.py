# -*- coding: utf-8 -*-

import requests
import config


class PushOver(object):

    def send_message_by_group(self, message, attachment=None, title=None):
        info_dict = {
            'token': config.token,
            'user': config.user,
            'message': message,
            'url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1545304526652&di=c3541f18d525f36ce0ec657e2972422e&imgtype=0&src=http%3A%2F%2Fimage2.suning.cn%2Fuimg%2Fb2c%2Fnewcatentries%2F0070072394-000000000141499311_1_800x800.jpg'
        }
        response = requests.post(config.url, info_dict)
        print(response)


if __name__ == '__main__':
    a = PushOver()
    res = a.send_message_by_group('hello world!')
    print(res)
