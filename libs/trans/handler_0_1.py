#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : trans_0_1
# __REFERENCES__ : https://blog.csdn.net/qq_42544196/article/details/106468658；https://docs.python.org/3/library/logging.html
# __date__: 2020/12/11 15
import datetime
import logging
from pathlib import Path
import random
import re
import sys
import threading
import time
from functools import wraps
from hashlib import md5
from typing import Any

import requests


def logger_set():
    """
    自定义日志格式，保存至对应文件
    官方文档：https://docs.python.org/3/library/logging.html
    """
    # 日志文件存储格式
    logger = logging.getLogger()
    logsf_loder = Path('./logs')
    # 如果目录不存在则创建
    logsf_loder.mkdir(parents=True, exist_ok=True)
    # 储存的文件名，带时间戳后缀
    logs_file = logsf_loder / \
        "{}.log".format(datetime.datetime.now().strftime('%y-%m-%d'))
    # 转为绝对路径
    fh = logging.FileHandler(logs_file.resolve(), encoding="utf-8", mode="a")
    logger.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(message)s\n"))
    logger.addHandler(fh)
    # 打印格式
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


logger_set()


class YouDaoFanYi(object):
    """
    引用于作者:https://blog.csdn.net/qq_42544196
    """

    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.138 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID="-1571440969@10.108.160.19"'
        }

    @staticmethod
    def create_data(e):
        n = "5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        t = md5(n.encode()).hexdigest()
        r = int(time.time() * 1000)
        i = int(str(r) + str(random.randint(0, 10)))
        sign = md5(("fanyideskweb" + e + str(i) +
                    "Nw(nmmbP%A-r6U3EUn]Aj").encode()).hexdigest()
        return {'ts': r, 'bv': t, 'salt': i, 'sign': sign}

    def fanyi_word(self, word):
        sys_data = self.create_data(word)
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'doctype': 'json',
            'version': 2.1,
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        result = requests.post(url=self.url, headers=self.headers, data={
                               **data, **sys_data}).json()
        # print(result)
        return result

    def main(self, word):
        self.fanyi_word(word)


def thread_handler(func):
    """
    TODO:多线程运行
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        pass

    return wrapper


class fanyi(YouDaoFanYi):
    """
    定制翻译对象
    """

    def _fanyi_word(self, word):
        res = self.fanyi_word(word=word)
        try:
            if res.get('translateResult'):
                smartResults = res.get('smartResult', {}).get('entries', [])
                results = [
                    re.sub("[\!\%\\t\\r\\n]", "", res)
                    for res in smartResults
                    if res
                ]
            rest = '\n  '.join([word]+results) if results else ''
            return rest
        except:
            pass

    def word_analysis_copy(self, *args: '翻译单个或多个单词', **kwds: Any):
        """
        """
        args = [' '.join(_.split('_')) if '_' in _ else _ for _ in set(args)]
        logging.info('\n'.join(map(self._fanyi_word, args)))

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.word_analysis_copy(*args)


"""
---------------------------------------------------------------------------
代码运行
>>> python .\main.py trans 
>>> trans
>>>  n. (Trans) （丹）唐（人名）
>>>  abbr. 交易；交易行为；交流；事务 (transaction)；及物的；（关系）可递的；过度的 (transitive)；（尤指职业）翻译；翻译程序；电 
>>>  视差频转播机 (translator)
>>>  adj. 反式的；跨性别的；（有机体）异型结合的
---------------------------------------------------------------------------
"""
# fanyi = fanyi()
# fanyi(*sys.argv[1:])
