# -*- coding: utf-8 -*-
#  __author__ : stray_camel
# __description__ :翻译工具启动器
# __REFERENCES__:
# __date__: 2021-02-22
import sys
from libs.trans.handler_0_1 import fanyi

_ = fanyi()
_(*sys.argv[1:])
