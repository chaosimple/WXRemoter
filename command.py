#!/usr/bin/env python
#coding:utf-8

"""
Purpose: 
    该模块定义 Command 类，用于定义系统支持的命令
Authors: 
    Chao -- < chaosimpler@gmail.com >
    
License: 
    LGPL clause

Created: 
    06/30/18
"""

from __future__ import division
import logging
import numpy as np
import pandas as pd

# 初始化日志对象
logger = logging.getLogger(__name__)


########################################################################
class Command(object):
    """
    """

    SCREENSHOT = u'给我截图'
    