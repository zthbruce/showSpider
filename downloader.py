# coding:utf-8

import sys
import re
import traceback
import logging
import logging.handlers
import MySQLdb

import requests
from lxml import html
reload(sys)
sys.setdefaultencoding('UTF-8')


if __name__ == "__main__":
    url = "http://www.youku.com"
    # 获取网页内容
    res = requests.get(url, timeout=10)
    print res.encoding
    res.encoding = "utf-8"
    text = res.content
    print text
    # print text
    _html = html.fromstring(text)
    css_selector = '#m_223473 > div > div:nth-child(2) > div.yk-pack.p-list.mb16 > ul.info-list > li.title.short-title > a'
    selector = _html.cssselect(css_selector)
    # selector = _html.find(css_selector)
    # selector = _html.xpath('//*[@id="block-G"]/div[1]/div/div[2]/ul/li[1]/a')
    print selector
    for ele in selector:
        print "here"
        # print html.tostring(ele)
        print ele.text
        print ele.get("href")




