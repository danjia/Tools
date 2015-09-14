# -*- coding: utf8 -*-
'''
@brief  利用plist的信息，将大图切成小图，并保存到相应的文件夹下面,
        只需要将该脚本放到png和plist所在的目录下然后运行就可以了
@author danjia 896560459@qq.com
@time   2015-09-03
'''
import os
import re
import xml.dom.minidom
from PIL import Image


#数字模式
global g_numberPattern
g_numberPattern = re.compile('(\d+)')

#目录和文件名分割模式
global g_pathPattern
g_pathPattern = re.compile("(.*)/.*")

'''
@brief 如果小图包含目录结构，建目录
'''
def buildFolder(path, smallPicName):
    global g_pathPattern
    result = g_pathPattern.findall(smallPicName)
    #如果小图还存在目录结构
    if len(result)>0 and not os.path.exists(path+'/'+result[0]):
        os.makedirs(path+'/'+result[0])


'''
@brief 裁剪图片
@param path            路径
       pngFileName     大图的路径
       smallPicName    小图的名字
       frame           小图在大图中的大小(左上角x坐标, 左上角y坐标, 宽, 高)
       offset          小图相对于大图需要的偏移量
       rotated         是否需要旋转
       sourceColorRect 原始小图的颜色矩形
       sourceSize      原始小图大小
'''
def interceptingPicture(path, pngFileName, smallPicName, frame, offset, rotated, sourceColorRect, sourceSize):
    img = Image.open(path+'/'+pngFileName)
    data = None
    if not rotated:
        data = img.crop((frame[0], frame[1], frame[0]+frame[2], frame[1]+frame[3]))
    else:
        data = img.crop((frame[0], frame[1], frame[0]+frame[3], frame[1]+frame[2]))
    newImg = None
    if not rotated:
        newImg = Image.new("RGBA", (sourceSize[0], sourceSize[1]))#, (1, 1, 1, 1))
    else:
        newImg = Image.new("RGBA", (sourceSize[1], sourceSize[0]))
    newImg.paste(data, (offset[0], offset[1]))
    if rotated:
        newImg = newImg.rotate(90)
    buildFolder(path+'/'+pngFileName[:-4], smallPicName)
    newImg.save(path+'/'+pngFileName[:-4]+'/'+smallPicName)

'''
@brief 处理单张小图
@param path         要解析的文件所在的路径
       pngFileName  大图的名字
       smallPicName 小图的名字
       onePicNode   小图的xml信息
'''
def onePic(path, pngFileName, smallPicName, onePicNode):
    frameStr           = None
    offsetStr          = None
    rotatedStr         = False
    sourceColorRectStr = None
    sourceSizeStr      = None
    
    key = None
    for item in onePicNode.childNodes:
        nodeName = item.nodeName
        if '#text' != nodeName:
            if 'key' == nodeName:
                key = item.firstChild.data
            else:
                if 'frame' == key:
                    frameStr = item.firstChild.data
                elif 'offset' == key:
                    offsetStr = item.firstChild.data
                elif 'rotated' == key:
                    if item.firstChild:
                        rotatedStr = item.firstChild.data
                    else:
                        rotatedStr = item.nodeName
                elif 'sourceColorRect' == key:
                    sourceColorRectStr = item.firstChild.data
                elif 'sourceSize' == key:
                    sourceSizeStr = item.firstChild.data

    global g_numberPattern
    frame           = g_numberPattern.findall(frameStr)
    offset          = g_numberPattern.findall(offsetStr)
    rotated         = "true"==rotatedStr
    sourceColorRect = g_numberPattern.findall(sourceColorRectStr)
    sourceSize      = g_numberPattern.findall(sourceSizeStr)
    interceptingPicture(
                        path,
                        pngFileName,
                        smallPicName,
                        (int(frame[0]),int(frame[1]),int(frame[2]),int(frame[3])),
                        (int(offset[0]), int(offset[1])),
                        rotated,
                        (int(sourceColorRect[0]), int(sourceColorRect[1]), int(sourceColorRect[2]), int(sourceColorRect[3])),
                        (int(sourceSize[0]),int(sourceSize[1])))

'''
@brief 处理N张小图
@param path        要解析的文件所在的路径
       pngFileName 大图的名字
       picListNode N张小图的xml信息
'''
def NPic(path, pngFileName, picListNode):
    # 建个文件夹存放N张小图
    folderName = pngFileName[:-4]
    if not os.path.exists(path+'/'+folderName):
        os.mkdir(path+'/'+folderName)
    
    smallPicName = None  
    for onePicNode in picListNode.childNodes:
        if onePicNode.nodeType == 1:
            if "key" == onePicNode.nodeName:
                smallPicName = onePicNode.firstChild.data
            elif "dict" == onePicNode.nodeName:
                onePic(path, pngFileName, smallPicName, onePicNode)

'''
@brief 处理单张png和plist
@param path          要解析的文件所在的路径
       plistFileName plist文件名
       pngFileName   png文件名
'''
def dealWithOnePngAndPlist(path, plistFileName, pngFileName):
    dom = xml.dom.minidom.parse(path+'/'+plistFileName)
    root = dom.documentElement
    dictNode = root.getElementsByTagName("dict")[0]

    # 处理N张小图
    picListNode = dictNode.getElementsByTagName("dict")[0]
    NPic(path, pngFileName, picListNode)

    # meta
    metadataListNode = dictNode.getElementsByTagName("dict")[1]

'''
@brief 利用plist文件的信息，把path路径下所有的png切出小图
@param path 要解析的文件所在的路径
'''
def translatePngToSmallPng(path):
    #path路径下所有文件名字
    fileList = os.listdir(path)
    for fileName in fileList:
        #筛选plist文件
        if -1!=fileName.find('.plist'):
            pngName = fileName[:-5]+'png'
            #查看是否存在对于的png文件
            if os.path.exists(pngName):
                print(pngName+'...')
                #处理单张png和plist
                dealWithOnePngAndPlist(path, fileName, pngName)
            else:
                print("error: not exists "+pngName)
        

if "__main__" == __name__:
    translatePngToSmallPng(".")
    print("done!!!")
