#!/usr/bin/env python
#coding:utf-8

"""
Purpose: 
    用于构建一个程序，接收微信的消息，进行相关操作；
    
Authors: 
    Chao -- < chaosimpler@gmail.com >
    
License: 
    MIT clause

Created: 
    06/30/18
"""

from __future__ import division
import logging
import numpy as np
import pandas as pd
import os

from PIL import ImageGrab

import itchat
from itchat.content import *

from command import Command

# 初始化日志对象
logger = logging.getLogger(__name__)


#----------------------------------------------------------------------
def send_screenshot_img(to_user):
    r""" 向指定用户发送当前屏幕截图
        
    Args:
        to_user : 要发送的用户名
    Returns:
        
    Raises:
        
    Note:
        
    """
    
    img_name = 'graph.png'
    
    # 对当前屏幕进行截图
    im = ImageGrab.grab()
    im.save(img_name)
    
    # 发送图片，并删除
    if itchat.send('@img@{}'.format(img_name), toUserName= to_user):
        os.remove(img_name)
    else:
        print u'发送失败！'
    
    
#----------------------------------------------------------------------
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    r""" 自动回复函数，用于对该微信号收到的消息进行处理
        
    Args:
        msg (message): 对消息的封装，参考：
        http://itchat.readthedocs.io/zh/latest/intro/messages/
        
    Returns:
        
    Raises:
        
    Note:
        
    """
    
    
    user_to = msg['FromUserName']
    if Command.SCREENSHOT in msg['Text']:
        send_img(user_to)
    
    else:
        pass

if __name__ == '__main__':
    
    itchat.auto_login(hotReload= True)
    itchat.run()
    
    pass
    