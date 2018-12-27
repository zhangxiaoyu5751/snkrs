# -*- coding: utf-8 -*-

import requests
import json
import config
import urllib.request, urllib.parse, urllib.error


def send_message(data_list):
    '''
        data = [{
                'shoe_uniq_desc':'asd',
                'shoe_name'
                'shoe_intro'
                'shoe_sell_time'
                'shoe_price'},
                {},
                {}]
    '''
    send_key = config.send_key
    text = '球鞋发售'
    total_md_str = ''''''
    for single_data in data_list:
        md_str = trans_dict_2_md(single_data) + '\n --- \n'
        total_md_str += md_str
    # desp = '''# 1\n## 44444 \n#### sdfffsdf\n![image](http://i01.lw.aliimg.com/media/lALPBbCc1ZhJGIvNAkzNBLA_1200_588.png)'''
    desp = total_md_str
    data = 'https://pushbear.ftqq.com/sub?sendkey={0}&text={1}&desp={2}'.format(send_key, urllib.parse.quote_plus(text),
                                                                                urllib.parse.quote_plus(desp))

    res = requests.get(data)


def trans_dict_2_md(single_shoe_info):
    shoe_name = single_shoe_info.get('shoe_name', '')
    shoe_intro = single_shoe_info.get('shoe_intro', '')
    shoe_sell_time = single_shoe_info.get('shoe_sell_time', '') if single_shoe_info.get(
        'shoe_sell_time') else u'发售中或发售结束'
    shoe_price = single_shoe_info.get('shoe_price','')
    shoe_pic = single_shoe_info.get('shoe_pic', '')
    md_str = '''# 球鞋名称:{shoe_name}\n## 球鞋发售时间:{shoe_sell_time}\n### 球鞋介绍：{shoe_intro}\n##### 球鞋发售价格：{shoe_price}\n![image]({shoe_pic})'''.format(
        shoe_name=shoe_name, shoe_intro=shoe_intro, shoe_sell_time=shoe_sell_time, shoe_price=shoe_price, shoe_pic=shoe_pic)
    return md_str


if __name__ == '__main__':
    # send_message(data_list=None)
    a = ''''''
    print(type(a))
