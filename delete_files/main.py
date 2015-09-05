# -*- coding: utf8 -*-
'''
@brief 批量删除操作
       (1)批量删除某个前缀文件
       (2)批量删除某个后缀文件
       (3)批量删除某个名字的文件
       (4)批量删除所有文件
'''

import os
import re
import sys

'''
@brief 匹配部分 matchType
'''
global PREFIX        #前缀匹配
global SUFFIX        #后缀
global ALL_FILE_NAME #整个文件名匹配
global EVERY_THING   #任何文件名都匹配
PREFIX        = 1
SUFFIX        = 2
ALL_FILE_NAME = 3
EVERY_THING   = 4


'''
@brief  获取即将删除的文件列表
@params path       处理哪个目录下的文件
        matchType  要删除的类型：
                   PREFIX(前缀), SUFFIX(后缀), ALL_FILE_NAME(删除整个文件名匹配), EVERY_THING(任何名字)
        keyWorld   要匹配的关键字
'''
def getGoingToDelFileList(path, matchType, keyWord=None):
    global PREFIX
    global SUFFIX
    global ALL_FILE_NAME
    global EVERY_THING
    curPath  = None
    pattern  = None

    #要删除的文件
    #[
    #  ("path1", [fileName1, fileName2, ...]),
    #  ("path2", [fileName1, fileName2, ...])
    #]
    delFilePathList = []
    #前缀匹配
    if PREFIX == matchType:
        pattern  = re.compile("^"+keyWord)
    #后缀匹配
    elif SUFFIX == matchType:
        pattern  = re.compile(keyWord+"$")
    #整个文件名匹配
    elif ALL_FILE_NAME == matchType:
        pattern  = re.compile("^"+keyWord+"$")
    #任何东西
    elif EVERY_THING == matchType:
        pattern  = re.compile(".*")
    else:
        pass
 
    scriptName = sys.argv[0].split("\\")[-1]
    for fileMsg in os.walk(path):
        curPath = fileMsg[0]
        delFileList = []
        for fileName in fileMsg[2]:
            result = pattern.findall(fileName)
            if len(result)>0:
                #如果匹配到的是本脚本，忽略掉
                if fileName == scriptName:
                    continue
                delFileList.append(fileName)
        if len(delFileList)>0:
            delFilePathList.append((curPath, delFileList))

    return delFilePathList

'''
@brief  删除文件
@params path       处理哪个目录下的文件
        matchType  要删除的类型：
                   PREFIX(前缀), SUFFIX(后缀), ALL_FILE_NAME(删除整个文件名匹配), EVERY_THING(任何名字)
        keyWorld   要匹配的关键字
'''
def deletFiles(path, matchType, keyWord=None):
    Y = y = True
    N = n = False
    isShow    = False
    isWantDel = False 
    #获取要删除的文件列表
    delFilePathList = getGoingToDelFileList(path, matchType, keyWord)

    #是否显示要删除的文件列表
    try:
        isShow = input(u"Show which file is going to delete?(y, n):")
    except:
        print("Wrong input!!!")
        return
    if isShow:
        for fileNameList in delFilePathList:
            print(fileNameList)

    #是否确认删除
    try:
        isWantDel = input(u"\nAre you sure to delete?(y, n):")
    except:
        print("Wrong input!!!")
        return
        
    if isWantDel:
        for filePathList in delFilePathList:
            for fileName in filePathList[1]:
                print("del "+fileName+'...')
                os.remove(filePathList[0]+'/'+fileName)
        print('\ndelete done!!!')

if "__main__" == __name__:
    #删除前缀为'abc'的文件
    deletFiles(".", PREFIX, 'abc')
    
    #删除后缀为'abc.txt'的文件
    #deletFiles(".", SUFFIX, 'abc.txt')

    #删除整个文件名匹配
    #deletFiles(".", ALL_FILE_NAME, 'aa.txt')

    #删除所有文件
    #deletFiles(".", EVERY_THING)
