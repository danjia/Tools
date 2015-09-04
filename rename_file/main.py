# -*- coding: utf8 -*-
'''
@brief 批量修改名字
'''
import os
import re
import sys

'''
@brief 处理新名字的模式
@param  newNamePattern 新名字的模式
@return 替换掉"?"的字符串
@example
    (1)输入:"abc?.txt"
       返回:"abc{}.txt"
    (2)输入:"abc???.txt"
       返回:"abc{:03}.txt"
'''
def dealWithNewName(newNamePattern):
    p =  re.compile("(\?+)")
    result = p.findall(newNamePattern)
    if len(result)>0:
        length = len(result[0])
        #一个"?"，表示不用补0
        if length == 1:
            newNamePattern = newNamePattern.replace(result[0], "{0}")
        #多个"?",按"?"的个数补零
        elif length > 1:
            newNamePattern = newNamePattern.replace(result[0], "{:0"+str(length)+"}")
        else:
            print("error")
    else:
        #print()
        assert('error:you need to set a pattern for newname, like "newName??.txt"' and False)
    return newNamePattern


'''
@brief 重命名所有文件
@params path             路径
        newNamePattern   新名字的模式
        renameStartIndex 新名字开始的索引
        renameStep       新名字的步长
'''
def renameAllFiles(path, newNamePattern, renameStartIndex, renameStep):
    #获取当前运行的脚步名字
    scriptName = sys.argv[0].split("\\")[-1]
    curPath  = None
    newName = dealWithNewName(newNamePattern)
    global g_scriptName
    for fileMsg in os.walk(path):
        curPath = fileMsg[0]
        for fileName in fileMsg[2]:
            #如果是当前运行的脚本，忽略掉
            if fileName == scriptName:
                continue
            os.rename(curPath+'/'+fileName, curPath+'/'+newName.format(renameStartIndex))
            renameStartIndex = renameStartIndex + renameStep


'''
@example:
(1)renameAllFiles(".", "abc?.png", 1, 1)
   abc1.png abc2.png abc3.png ...
   
(2)renameAllFiles(".", "abc????.png", 1, 1)
   abc0001.png abc0002.png abc0003.png ...
'''

if "__main__" == __name__:
    renameAllFiles(".", "danjia??.txt", 1, 1)
