#coding:utf-8

import os
import shutil
import Config
import Common

def makeRoot():
	if os.path.exists(Config.getOutPath()):
	    shutil.rmtree(Config.getOutPath())
	os.mkdir(Config.getOutPath())

#创建工程目录
def makeLibDir(fromName, outName):
	#创建SDK根目录
	sdkLib = os.path.join(Config.getOutPath(),outName)
	if os.path.exists(sdkLib) == False:
		os.mkdir(sdkLib)

	# 创建libs目录
	libs = sdkLib + "/libs"
	if os.path.exists(libs) == False:
	    os.mkdir(libs)
	#创建Src目录
	src = sdkLib + "/src"
	if os.path.exists(src) == False:
	    os.mkdir(src)

	main = sdkLib+"/src/main"
	if os.path.exists(main) == False:
	    os.mkdir(main)
	copy(fromName,outName)


def makeSDKDemo(fromName, outName):
    # 创建SDK根目录
    sdkLib = os.path.join(Config.getOutPath(), outName)
    if os.path.exists(sdkLib) == False:
        os.mkdir(sdkLib)

    # 创建libs目录
    targetlibs = sdkLib + "/libs"
    if os.path.exists(targetlibs) == False:
        os.mkdir(targetlibs)
    # 创建Src目录
    targetsrc = sdkLib + "/src"
    if os.path.exists(targetsrc) == False:
        os.mkdir(targetsrc)

    if os.path.exists(Config.getSrcPath() + fromName+"/libs"):
        Common.copyFiles(Config.getSrcPath() + fromName + "/libs", targetlibs)
    if os.path.exists(Config.getSrcPath() + fromName+"/src"):
        Common.copyFiles(Config.getSrcPath() + fromName + "/src", targetsrc)

    shutil.copy(Config.getSrcPath() + fromName +"/build.gradle", Config.getOutPath() + outName)
    shutil.copy(Config.getSrcPath() + fromName +"/proguard-rules.pro", Config.getOutPath() + outName)
	
#将文件移动到目标文件夹
def copy(fromName,outName):
	copyXmlToMain(fromName,outName)
	copyGradleToLib(fromName,outName)
	copyJarToLibs(fromName,outName)
	
#移动AndroidManifest
def copyXmlToMain(fromName,outName):
    xmlPath = Config.getSrcPath()+fromName+"/src/main/AndroidManifest.xml"
    print(xmlPath)
    shutil.copy(xmlPath,Config.getOutPath()+outName+'/src/main')

#moveXmlToMain()
	
#移动build.gradle
def copyGradleToLib(fromName,outName):
    gradlePath = Config.getSrcPath()+fromName+"/build.gradle"
    print(gradlePath)
    shutil.copy(gradlePath,Config.getOutPath()+outName)

#moveGradleToLib()

#移动jar包
def copyJarToLibs(fromName,outName):
    #遍历该目录下所有的文件进行移动
    libsPath = Config.getSrcPath()+fromName+"/libs/"
    Common.copyFiles(libsPath, Config.getOutPath() + outName + '/libs/')

