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
def get_user_name(msg):
    r"""获取发送该 msg 用户的名称
        
    Args:
        
    Returns:
        
    Raises:
        
    Note:
        
    """
    user_name = ''
    
    if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:
        #优先使用备注名称
        user_name = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
    else:
        #在好友列表中查询发送信息的好友昵称 
        user_name = itchat.search_friends(userName=msg['FromUserName'])['NickName']    
    
    
    return user_name
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
# 这里的TEXT表示如果有人发送文本消息()
# TEXT  文本  文本内容(文字消息)
# MAP  地图  位置文本(位置分享)
# CARD  名片  推荐人字典(推荐人的名片)
# SHARING  分享  分享名称(分享的音乐或者文章等)
# PICTURE 下载方法    图片/表情
# RECORDING  语音  下载方法
# ATTACHMENT  附件  下载方法
# VIDEO  小视频  下载方法
# FRIENDS  好友邀请  添加好友所需参数
# SYSTEM  系统消息  更新内容的用户或群聊的UserName组成的列表
# NOTE  通知  通知文本(消息撤回等)，那么就会调用下面的方法
# 其中isFriendChat表示好友之间，isGroupChat表示群聊，isMapChat表示公众号

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    r""" 自动回复函数，用于对该微信号收到的消息进行处理
        
    Args:
        msg (message): 对消息的封装，参考：
        http://itchat.readthedocs.io/zh/latest/intro/messages/
        
    Returns:
        
    Raises:
        
    Note:
        
        通过打印 itchat 的用户以及注册消息的参数, 可以发现这些值都是字典.
        但实际上 itchat 精心构造了相应的消息,用户,群聊,公众号等.
        其所有的键值都可以通过这一方式访问:
    
        @itchat.msg_register(TEXT)
        def _(msg):
            # equals to print(msg['FromUserName'])
            print(msg.fromUserName)
    
        属性名为键值首字母小写后的内容.
    
        author = itchat.search_frients(nickName="LittleCoder")[0]
        author.send("greeting ,  LittleCoder!")        


    """
    
    # 发送该消息的用户名
    to_user_id = msg['FromUserName']
    to_user_name = get_user_name(msg)
    
    if Command.SCREENSHOT in msg['Text']:
        send_screenshot_img(to_user_id)
    
    else:
        pass



#----------------------------------------------------------------------
@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    r""" 群消息的捕获 和 处理；
        
    Args:
        msg (message): 对消息的封装，参考：
        http://itchat.readthedocs.io/zh/latest/intro/messages/
        
    Returns:
        
    Raises:
        
    Note:
        群必须保存到通讯录中，否则无法正确获取群信息；
    """
    
    # 根据群消息的FromUserName匹配是哪个群
    group = itchat.search_chatrooms(userName= msg['FromUserName'])
    
    # 构造 该群 的基本信息字符串
    if group is not None:
        group_name = group['NickName']
        group_menbers = group['MemberCount']    
        str_group_name = group_name + "(" + str(group_menbers) +")"
    else:
        str_group_name = '(None)'
    
    # 如果是 @我 的话
    # 进行处理
    if msg['isAt']:
        
        str_msg = u'@%s\u2005%s' % (msg['ActualNickName'], u'收到：' + msg['Text'])
        return str_msg
    

if __name__ == '__main__':
    
    itchat.auto_login(hotReload= True)
    itchat.run()
    
    pass
    