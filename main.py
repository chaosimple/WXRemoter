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
from os_operator import OSOperator

# 初始化日志对象
logger = logging.getLogger(__name__)

# 任务系统是否开启
BG_SYS_START = False
# 自动回复是否开启
BG_SYS_AUTO_REPLY_START = False

# 上一个消息发送者的 ID
LAST_MSG_SENDER_ID = None


#----------------------------------------------------------------------
def get_user_name(user_id, use_remark_name_first = True):
    r"""根据用户 ID 获取名称 （只针对个人）
        
    Args:
        user_id (string) : 用户 id；
        use_remark_name_first (bool, optional): 是否优先使用备注名，默认为True;
    Returns:
        user_name (string): 用户名称；
    """
    user_name = ''
    user = itchat.search_friends(userName= user_id)
    
    user_name = user['NickName']
    if use_remark_name_first and user.get('RemarkName'):
        user_name = user['RemarkName']
        
    return user_name
    
    
#----------------------------------------------------------------------
def send_screenshot_img(id_user):
    r""" 向指定用户发送当前屏幕截图
        
    Args:
        to_user : 要发送的用户ID
    """
    
    img_name = 'graph.png'
    
    # 对当前屏幕进行截图
    im = ImageGrab.grab()
    im.save(img_name)
    
    # 发送图片，并删除
    if itchat.send('@img@{}'.format(img_name), toUserName= id_user):
        os.remove(img_name)
    else:
        print u'发送失败！'
    


#----------------------------------------------------------------------
def do_sys_task(str_msg):
    r"""根据命令字符串，用于执行系统命令
        
    Args:
        str_msg (string): 以 '@st' 开始的命令字符串；
    Returns:
        
    Raises:
        
    Note:
        执行一系列的系统命令，步骤如下：
        1. 首先发送 @ststart 命令开启命令系统；
        2. 执行 @stXXX 相关命令；
        3. 使用 @stclose 命令退出命令系统；
        
        由于涉及对系统文件的操作，为了防止误操作，需要先开启命令系统，才能接收相关指令；
        命令系统处于关闭状态时不执行相关命令，防止误操作；
    """
    
    str_help = u"\n系统命令:\n"+\
        u"{} 开始系统\n".format(Command.SYS_OPT_START)+\
        u"@stclose 关闭系统\n"+\
        u"@stshutdown 关闭服务器\n" +\
        u"@stcopy 拷贝文件" +\
        u"{} 开始自动回复\n".format(Command.SYS_OPT_START_AUTO_REPLY) +\
        u"{} 关闭自动回复\n".format(Command.SYS_OPT_CLOSE_AUTO_REPLY)
    
    # 标明命令系统是否处于开启状态
    # 声明该变量采用全局变量
    global BG_SYS_START
    
    # 标记自动回复是否开启
    global BG_SYS_AUTO_REPLY_START
    
    
    if str_msg == Command.SYS_OPT_START:
        BG_SYS_START = True
        return u'命令系统已开启\n准备执行相关系统命令'
    
    if str_msg == Command.SYS_OPT_CLOSE:
        BG_SYS_START = False
        return u'命令系统已关闭'
    
    
    if not BG_SYS_START:
        str_msg = u' 还未启动系统，请先启动系统！'
        str_msg += str_help
        return str_msg
    
    
    # 执行相关操作
    if str_msg == Command.SYS_OPT_SHUTDOWN:
        OSOperator.shutdown()
    elif str_msg == Command.SYS_OPT_CPYFILE:
        if OSOperator.copy_file(Command.SRC_DIR_PATH,
                             Command.DST_DIR_PATH):
            return u'文件拷贝完成'
    elif str_msg == Command.SYS_OPT_START_AUTO_REPLY:
        BG_SYS_AUTO_REPLY_START = True
        return u' 开启自动回复'
    elif str_msg == Command.SYS_OPT_CLOSE_AUTO_REPLY:
        G_WHO_SEND = None
        BG_SYS_AUTO_REPLY_START = False
        return u'自动回复已关闭'
    
    else:
        # 如果不能正常解析该命令
        # 则返回帮助
        return str_help



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

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING], isFriendChat= True)
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
    global LAST_MSG_SENDER_ID
    

    # 发送该消息的用户名
    from_user_id = msg['FromUserName']
    from_user_name = get_user_name(from_user_id)
    
    to_user_id = msg['ToUserName']
    to_user_name = get_user_name(to_user_id)
    
    self_id = itchat.get_friends(update = True)[0]['UserName']
    self_name = get_user_name(self_id)
    
    # 文本消息
    str_msg = msg['Text']
    
    # 截图命令
    if Command.SCREENSHOT in str_msg:
        send_screenshot_img(from_user_id)
    
    
    # 如果命令是系统命令
    # 则根据系统状态，执行相关指令
    if str_msg.startswith(Command.SYS_OPT):
        return do_sys_task(str_msg)
    
    if to_user_id == self_id:
        # 标记自动回复是否开启
        global BG_SYS_AUTO_REPLY_START        
        
        if BG_SYS_AUTO_REPLY_START:
            LAST_MSG_SENDER_ID = from_user_id
            # 发送给小冰
            xiaoice = itchat.search_mps(name= u'小冰')[0]['UserName']
            itchat.send(str_msg, xiaoice)
    

#----------------------------------------------------------------------
@itchat.msg_register([TEXT],  isMpChat=True)
def mp_auto_reply(msg):
    r""" 对公众号的消息自动回复，实现将小冰回复的信息转发给上次给我发送消息的人
        
    """
    from_user_id = msg['FromUserName']
    from_user_name = msg['User']['NickName']
    
    to_user_id = msg['ToUserName']
    to_user_name = get_user_name(to_user_id)    

    global LAST_MSG_SENDER_ID
    global BG_SYS_AUTO_REPLY_START
    
    if BG_SYS_AUTO_REPLY_START:
        xiaoice = itchat.search_mps(name= u'小冰')[0]['UserName']
        if from_user_id == xiaoice:
            itchat.send(msg['Text'], toUserName=LAST_MSG_SENDER_ID)
    


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
    
    #itchat.auto_login(hotReload= True, enableCmdQR= 2)
    itchat.auto_login(hotReload= True)
    
    itchat.run()

    pass
    