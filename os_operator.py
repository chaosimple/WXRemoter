#!/usr/bin/env python
#coding:utf-8

"""
Purpose: 
    该模块用于执行一系列定义的系统操作任务
Authors: 
    Chao -- < chaosimpler@gmail.com >
    
License: 
    LGPL clause

Created: 
    07/01/18
"""

from __future__ import division
import logging
import os
import datetime

# 初始化日志对象
logger = logging.getLogger(__name__)


########################################################################
class OSOperator(object):
    """
    """

    #----------------------------------------------------------------------
    @classmethod
    def make_zip(cls, source_path):
        r""" 对指定目录或者文件进行打包压缩为一个 zip 文件
            
        Args:
            source_path (string): 待压缩的 目录路径 或者 文件路径；
        Returns:
            output_filename (string): 压缩后的文件绝对路径；
            
            如果失败，则返回 None；
        Example:
            >>> dir_path = '/Users/chao/Desktop/test/cmp'
            >>> file_path = '/Users/chao/Desktop/test/dp_cluster_data.csv'
            >>> 
            >>> zip_file = OSOperator.make_zip(dir_path)        # 压缩目录
            >>> zip_file = OSOperator.make_zip(file_path)       # 压缩文件
            >>> if zip_file is not None:
            >>>     print 'Zip completed, zip file stored in:\n{}'.format(zip_file)
            >>> 
        Note:
            根据传入的路径，在同目录下自动生成压缩文件名称；
            
        """
        
        import zipfile
        
        # 如果要压缩的路径不存在，则直接返回
        if not os.path.exists(source_path):
            return None
        
        
        # 构造压缩文件的名称
        parent_dir = os.path.abspath(os.path.join(source_path , os.pardir))
        output_filename = os.path.join(parent_dir,
                                       '{}_{}.zip'.format(source_path.split(os.path.sep)[-1],
                                       datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')))                

        # 对文件夹进行压缩
        if os.path.isdir(source_path):
            
            pre_len = len(os.path.dirname(source_path))
            try:
                with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for parent, dirnames, filenames in os.walk(source_path):
                        for filename in filenames:
                            pathfile = os.path.join(parent, filename)
                            arcname = pathfile[pre_len:].strip(os.path.sep)     #相对路径
                            zipf.write(pathfile, arcname)
            except Exception as e:
                #raise ('Zip error!' + e.message)
                return None
        
        
        # 对文件进行压缩
        elif os.path.isfile(source_path):
            try:
                with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    arc_name = os.path.basename(source_path)                 
                    zipf.write(filename = source_path, arcname = arc_name)
            except Exception as e:
                return None
        
        
        return output_filename
    
    
    #----------------------------------------------------------------------
    @classmethod
    def shutdown(self):
        r"""关闭系统
            
        Args:
            
        Returns:
        
        Raises:
            
        Note:
            
        """
        print 'shutdown -s -f -t 1'
        #os.system('shutdown -s -f -t 1')        
        
       
        

    #----------------------------------------------------------------------
    @classmethod
    def copy_file(self, src_file, dst_file):
        r"""关闭系统
            
        Args:
            
        Returns:
        
        Raises:
            
        Note:
            
        """
        #import shutil
        #shutil.copytree('F:/12', 'F:/14')
        print "copytree('F:/12', 'F:/14')"
        return True
