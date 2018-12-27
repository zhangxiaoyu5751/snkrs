# -*- coding: utf-8 -*-

import snkrs
from docopt import docopt
import alert_over
from datetime import datetime, timedelta
import lib_sqlite
import config
import datetime
import send_mess_by_push_bear

# 转换时间方法
def trans_time(regular_time):
    date_ = datetime.strptime(regular_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_time = date_ + timedelta(hours=8)
    return local_time


# 将字典列表转换成字符串
def conver_list_2_str(data_list):
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
    a = ' '
    final_str = ''
    str_list = []
    for single_shoe_data in data_list:
        single_shoe_dict = dict()
        single_shoe_dict[u'球鞋名称'] = single_shoe_data.get('shoe_name')
        single_shoe_dict[u'球鞋介绍'] = single_shoe_data.get('shoe_intro')
        single_shoe_dict[u'球鞋发售时间'] = single_shoe_data.get('shoe_sell_time') if single_shoe_data.get(
            'shoe_sell_time') else u'发售中或发售结束'
        single_shoe_dict[u'球鞋发售价格'] = single_shoe_data.get('shoe_price')
        single_str = ''
        for k, v in single_shoe_dict.items():
            single_str += ''.join([k, ':', v, a * 32])
        str_list.append(single_str)

    for x in str_list:
        final_str += ''.join([x, a * 6])

    return final_str


# 把不合法以及不完整的的dict过滤掉
def filter_empty_dict(single_shoe_info):
    pass


def is_empty(data):
    is_empty_flag = True
    if isinstance(data, str) or isinstance(data, (int, float, bool)):
        is_empty_flag = False if data else True
    elif isinstance(data, list):
        if not data:
            is_empty_flag = True
        for item in data:
            result = is_empty(item)
            if not result:
                is_empty_flag = False
                break
    elif isinstance(data, dict):
        if not data:
            is_empty_flag = True
        for k, v in data.items():
            result = is_empty(v)
            if not result:
                is_empty_flag = False
                break
    return is_empty_flag


# 检查数据是不是存在于今天的数据表中 如果不存在 则
def check_data_in_db(conn_sqlite, data):
    shoe_uniq_desc = data.get('shoe_uniq_desc', '') if data.get('shoe_uniq_desc', '') else ''
    # 如果传过来的数据没有 唯一标识desc， 那么则不做检查
    shoe_name = data.get('shoe_name', '') if data.get('shoe_name', '') else ''
    if not (shoe_uniq_desc and shoe_name):
        return True
    sql = '''select * from shoe_info where shoe_uniq_desc ="{0}" and update_time > "{1}"'''.format(shoe_uniq_desc,
                                                                                     datetime.datetime.now().strftime(
                                                                                         '%Y-%m-%d'))
    query_result = conn_sqlite.query_one(sql)
    return True if query_result[1] else False


# 将数据插入到sqlite中
def insert_shoe_info_2_db(conn_sqlite, data):
    '''
    'shoe_uniq_desc'
    'shoe_name'
    'shoe_intro'
    'shoe_sell_time'
    'shoe_price'
    '''
    shoe_uniq_desc = data.get('shoe_uniq_desc', '') if data.get('shoe_uniq_desc', '') else ''
    if not shoe_uniq_desc:
        return False
    shoe_name = data.get('shoe_name', '') if data.get('shoe_name', '') else ''
    shoe_intro = data.get('shoe_intro', '') if data.get('shoe_intro', '') else ''
    shoe_sell_time = data.get('shoe_sell_time', '') if data.get('shoe_sell_time', '') else ''
    shoe_price = data.get('shoe_price', '') if data.get('shoe_price', '') else ''
    shoe_pic = data.get('shoe_pic', '') if data.get('shoe_pic', '') else ''

    sql = '''insert into shoe_info (shoe_uniq_desc, shoe_name, shoe_intro, shoe_sell_time, shoe_price, shoe_pic) values("{0}","{1}","{2}","{3}","{4}","{5}")'''.format(
        shoe_uniq_desc, shoe_name, shoe_intro, shoe_sell_time, shoe_price, shoe_pic)

    insert_result = conn_sqlite.insert(sql)

    return True if insert_result[0] else False


def get_all_shoe_info(conn_sqlite):
    sql = " select * from shoe_info where update_time >'{0}'".format(datetime.datetime.now().strftime('%Y-%m-%d'))
    query_result = conn_sqlite.query_all(sql)
    final_result = list()
    for item in query_result[1]:
       
        shoe_dict = dict()
        shoe_dict['shoe_uniq_desc'] = item[1]
        shoe_dict['shoe_name'] = item[2]
        shoe_dict['shoe_intro'] = item[3]
        shoe_dict['shoe_sell_time'] = item[4]
        shoe_dict['shoe_price'] = item[5]
        shoe_dict['shoe_pic'] = item[6]
        final_result.append(shoe_dict)
    return final_result


def main(send_method):
    conn_sqlite = lib_sqlite.ConnSqlite(config.db_info)
    send_robot = alert_over.AlertOver()
    snkrs_instance = snkrs.Snkrs()
    up_coming_single_shoe_url_list = snkrs_instance.get_upcoming_url_list()
    shoe_dict_info = list()
    for shoe_url in up_coming_single_shoe_url_list:
        shoe_detail_dict = snkrs_instance.get_detail_info_by_url(shoe_url)
       
        if is_empty(shoe_detail_dict):
            continue
        shoe_dict_info.append(shoe_detail_dict)
    # 流式推送今天的数据
    if send_method == 'stream':
        send_message = list()
        # [{},{},{}]
        for single_shoe_detail in shoe_dict_info:
            # 如果数据存在数据库中
            if check_data_in_db(conn_sqlite, single_shoe_detail):
                continue
            # 如果不存在数据库中 那么 写入数据库 并进行推送
            insert_shoe_info_2_db(conn_sqlite, single_shoe_detail)
            send_message.append(single_shoe_detail)
        if send_message:
            send_mess_by_push_bear.send_message(send_message)
            # trans_message = conver_list_2_str(send_message)
            #send_robot.send_message(trans_message.strip())

    # 全量推送今天的数据
    if send_method == 'batch':
        all_shoe_info = get_all_shoe_info(conn_sqlite)
        if all_shoe_info:
            #trans_message = conver_list_2_str(all_shoe_info)
            send_mess_by_push_bear.send_message(all_shoe_info)
            #send_robot.send_message(trans_message.strip())


if __name__ == '__main__':
    usage = """main

    Usage:
      main.py (-h | --help)
      main.py (-v | --version)
      main.py --method=send_method

    Options:
      -h --help             帮助
      -v --version          版本
      --method=send_method  推送方式 分为增量推送和全量推送  batch/stream

    """
    arguments = docopt(usage, version='1.0')
    send_method = arguments.get('--method')
    main(send_method)
