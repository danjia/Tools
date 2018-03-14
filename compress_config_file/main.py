# -*- coding:utf-8 -*-
#=======================================
# @brief 对配置文件(plist, exportJson)
#        进行压缩
#=======================================
import os

#======================================
# @brief 压缩文件并覆盖文件(不可逆)
#======================================
def compressConfigFile(configPath):
	for prePath, _, fileNameList in os.walk(configPath):
		for fileName in fileNameList:
			# 文件名包含(.plist 和 .ExportJson)
			if -1!=fileName.find(".plist") or -1!=fileName.find(".ExportJson"):
				data = ""
				cnt = 0
				f = open(prePath+'/'+fileName, "rb")
				for lineData in f.readlines():
					cnt = cnt + 1
					# 忽略掉包含.png 和.jpg 的那些行,有可能命名不规范
					if -1 != lineData.find(".png") or -1 != lineData.find(".jpg"):
						data = data + lineData
					else:
						# 忽略前面5行(那些配置的相关信息)
						if cnt > 5:
							data = data + lineData.replace(" ", "").replace("\n", "").replace("\r", "")
						else:
							data = data + lineData.replace("\n", "").replace("\r", "")
				f.close()
				data = data.replace("\n", "").replace("\r", "")
				
				fw = open(prePath+'/'+fileName, "wb")
				data = fw.write(data)
				fw.close()


if "__main__" == __name__:
	compressPath = "./needCompressPath"
	print(u"确定压缩文件"),
	choice = raw_input(u"[y/n]:")
	if "Y" == choice or "y" == choice:
		compressConfigFile(compressPath)
	elif "N"!=choice or "n" == choice:
		print(u"输入不合法")

	


