import re
import Config
import os
import shutil

def handleXLSDK(gradleFile):
    file = open(gradleFile, 'r')
    content = file.read()
    file.close()

    pattarn = "dependencies {(.*?)}";
    tStr = "\n   implementation fileTree(include: ['*.jar'], dir: 'libs')\n"
    content1 = re.findall(pattarn, content, flags=re.DOTALL)
    content = content.replace(content1[0], tStr)
    file = open(gradleFile, 'w')
    file.write(content)
    file.close()

def handlePlugin(gradleFile):
    file = open(gradleFile, 'r')
    content = file.read()
    file.close()

    pattarn = "dependencies {(.*?)}"
    tStr = "\n   implementation fileTree(include: ['*.jar'], dir: 'libs')\n"
    content1 = re.findall(pattarn, content, flags=re.DOTALL)
    content = content.replace(content1[0], tStr)
    file = open(gradleFile, 'w')
    file.write(content)
    file.close()

def handleDemo(gradleFile):
    file = open(gradleFile, 'r')
    content = file.read()
    file.close()

    pattarn = "dependencies {(.*?)}"
    tStr = "\n   implementation fileTree(include: ['*.jar'], dir: 'libs')\n   implementation project(':XLSdkLib')\n   implementation project(':xiaomiPlugin')\n   implementation 'com.android.support:appcompat-v7:26.1.0'\n";
    content1 = re.findall(pattarn, content, flags=re.DOTALL)
    content = content.replace(content1[0], tStr)
    file = open(gradleFile, 'w')
    file.write(content)
    file.close()

def createRootNeedGradles():
    file = open(Config.getOutPath()+"/settings.gradle", 'w')
    content = "include ':XLSDKDemo', ':xiaomiPlugin', ':XLSdkLib'"
    file.write(content)
    file.close()

    shutil.copy(Config.getSrcPath()+"/build.gradle", Config.getOutPath())