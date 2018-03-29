# -*- coding: utf-8 -*-
"""modified smali for channel sdk"""
import os
import re
import shutil
import fileinput

import HandleFile
import Common
import HandleIni

def mergeSmali(srcfolder, destfolder,configfile):
    print 'srcfolder '+ srcfolder + ' destfolder ' + destfolder
    handlerU3Djar(configfile,srcfolder)
    HandleFile.mergedir(srcfolder, destfolder)

"""
smaliFolder must be: xxx/smali
    just like: xxx/smali
packagename like: com.huanlexiyou.mi or com/huanlexiyou/mi
"""
def modifySmali(smaliFolder, oldPackageName, newPackageName):
    deleteDummySmail(smaliFolder)
    oldPackageName = oldPackageName.replace('.', '/')
    newPackageName = newPackageName.replace('.', '/')
    #modifyPackageName(smaliFolder + '/' + oldPackageName, oldPackageName, newPackageName)
    channelHooks(smaliFolder)

def modifyPackageName(smaliFolder, oldPackageName, newPackageName):
    if newPackageName == '' or newPackageName == None:
        Common.Msg('newPackageName is null, no need to modify packagename.')
        return
    for file in os.listdir(smaliFolder):
        if re.search(r'R\$*\w*\.smali', file) or (not re.search(r'\w*\.smali', file)):
            continue
        filePath = os.path.join(smaliFolder, file)
        if os.path.isfile(filePath):
            changePackageName(filePath, oldPackageName, newPackageName)
        else:
            modifyPackageName(filePath, oldPackageName, newPackageName)
    modifyPath(smaliFolder, oldPackageName, newPackageName)    

#����΢��֧�����
def modifyWXPackageName(smaliFolder,newPackageName):
    print 'modifyWXPackageName smaliFolder ' + smaliFolder
    if newPackageName == '' or newPackageName == None:
        Common.Msg('newPackageName is null, no need to modify packagename.')
        return
    oldPackageName = 'com.duowan.fxsdk.plugin.wxapi'
    newPackageName = newPackageName + '.wxapi'
    oldPackageName = oldPackageName.replace('.', '/')
    newPackageName = newPackageName.replace('.', '/')
    print 'replace ' + oldPackageName + ' packagename to ' + newPackageName
    olderfilePath = os.path.join(smaliFolder, oldPackageName)
    print 'modifyWXPackageName olderfilePath ' + olderfilePath
    if os.path.exists(olderfilePath):
        modifyPackageName(olderfilePath, oldPackageName, newPackageName)
    else:
        print 'not exists folder ' + olderfilePath

def changePackageName(smaliFile, oldPackageName, newPackageName):
    #TODO(qingcui) This way to update file may be slow
    file = open(smaliFile, 'r')
    content = file.read()
    file.close()
    content = content.replace(oldPackageName, newPackageName)
    file = open(smaliFile, 'w')
    file.write(content)
    file.close()

def modifyPath(smaliFolder, oldPackageName, newPackageName):
    tempDir = Common.GetTempDir() + 'smailtemp'
    if os.path.exists(tempDir):
        Common.Msg(tempDir + 'is exists, delete for move')
        shutil.rmtree(tempDir)
    shutil.move(smaliFolder, tempDir)

    pathList = smaliFolder.split(oldPackageName)
    newPath = pathList[0] + newPackageName
    if os.path.exists(newPath):
        Common.Msg(newPath + 'is exists, delete for move') 
        shutil.rmtree(newPath)
    shutil.move(tempDir, newPath)
    Common.Msg('change path\n\tfrom:' + smaliFolder + '\n\t  to:' + newPath)

def deleteDummySmail(smaliFolder):
    dels = ['/com/xiaomi' , '/com/xlpay/sdk/mipaylib' , '/com/xlpay/sdk/xiaomipay' , '/com/xlpay/sdk/plugin']
    for subpath in dels:
        deleteDir = smaliFolder + subpath
        if os.path.exists(deleteDir):
            shutil.rmtree(deleteDir)

def channelHooks(smaliFolder):
    file = smaliFolder + '/cn/uc/gamesdk/d/a.smali'
    Common.Msg(file)
    if os.path.exists(file):
        for line in fileinput.input(file, inplace = True):
            if not re.search('setDefaultUncaughtExceptionHandler', line):
                print line

def handlerU3Djar(configfile,smaliFolder):
    channelid = HandleIni.GetValueByKey(configfile, 'GLOBAL_CHANNEL_ID')
    if channelid == '10009':
       enginetype = HandleIni.GetValueByKey(configfile, 'ENGINE_TYPE')
       if enginetype == 'Unity3D':
          deleteDir1 = smaliFolder + '/com/unity3d'
          deleteDir2 = smaliFolder + '/org/fmod'
          if os.path.exists(deleteDir1):
              shutil.rmtree(deleteDir1)
          if os.path.exists(deleteDir2):
              shutil.rmtree(deleteDir2)