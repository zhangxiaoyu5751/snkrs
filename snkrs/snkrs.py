# -*- coding: utf-8 -*-
import os
import re
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from pyquery import PyQuery as pq

import config


class Snkrs(object):

    def get_upcoming_url_list(self):
        response = requests.get(config.SNKRS_URL, headers=config.headers)
        soup = bs(response.content, "html.parser")
        name_list = soup.findAll("div", {"class": "ncss-col-sm-12 full"})
        up_coming_single_shoe_url = set()
        for name in name_list:
            for link in name.find_all('a'):
                if len(link.get('href').split('/')) >= 4:
                    if link.get('href').split('/')[3] == 't':
                        up_coming_single_shoe_url.add(config.ORIGIN_URL + link.get('href'))
        return up_coming_single_shoe_url

    def get_detail_info_by_url(self, url):
        shoe_detail_info = dict()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--headless")
        driver_path = os.path.join("/home/snkrs_project/snkrs","chromedriver")

        driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
        ##########################################
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--disable-extensions')
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument('--no-sandbox')
        #driver = webdriver.Chrome(chrome_options = chrome_options)
        #########################################################################
        #driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')
        driver.get(url)
        page_content = driver.page_source
        trans_content = pq(page_content)
        a = trans_content('.product-info.ncss-col-sm-12').children()
        #print(trans_content)
        shoe_pic_query = trans_content('.u-cursor-pointer')
        # print(a)  # 用 h1  和  h5  区别
        h1_content = " ".join(self.get_h1_content(a).split())
        # print('h1', h1_content)
        h5_content = " ".join(self.get_h5_content(a).split())
        # print('h5', h5_content)
        sell_time = self.get_sell_time(a)
        # print(sell_time)
        sell_price = self.get_sell_price(a)
        # print(sell_price)
        shoe_pic = self.get_shoe_pic(shoe_pic_query)
        shoe_detail_info.update({
            'shoe_uniq_desc': url.rsplit('/')[-2],
            'shoe_name': h5_content,
            'shoe_intro': h1_content,
            'shoe_sell_time': sell_time,
            'shoe_price': sell_price,
            'shoe_pic': shoe_pic
        })
        return shoe_detail_info

    # 获取h1标签里面的内容
    def get_h1_content(self, data):
        html_h1 = re.findall(r"<h1.*?>(.*?)</h1>", str(data), re.S | re.M)
        return html_h1[0] if html_h1 else ''

    # 获取h5标签里面的内容
    def get_h5_content(self, data):
        html_h5 = re.findall(r"<h5.*?>(.*?)</h5>", str(data), re.S | re.M)
        return html_h5[0] if html_h5 else ''

    # 获取发售时间
    def get_sell_time(self, data):
        html_sell_time = re.findall(r"<div.*?test-available-date.*?>.*?>(.*?)</div>", str(data), re.S | re.M)
        return html_sell_time[0] if html_sell_time else ''

    # 获取发售价格
    def get_sell_price(self, data):
        html_sell_price = re.findall(r"</h5>.*?>(.*?)</div>", str(data), re.S | re.M)
        return html_sell_price[0] if html_sell_price else ''
   
   # 获取球鞋图片
    def get_shoe_pic(self, data):
        html_shoe_pic = re.findall(r'''<img src="(.*?)" alt''', str(data), re.S | re.M)
        return html_shoe_pic[0] if html_shoe_pic else ''


if __name__ == '__main__':
    a = Snkrs()
    b = a.get_upcoming_url_list()
    for item in b:
        print(item)
        c = a.get_detail_info_by_url(item)
        print(c)



