# -*- coding: utf-8 -*-
"""
"""
import sys
import os
import platform
import inspect
import re
import shutil

import Common

def CopyFiles(sourceDir, targetDir):
    if not os.path.exists(sourceDir) and not os.path.exists(targetDir):
        Common.ErrorMsg('copy Files from %s to %s Fail:file not found' % (sourceDir, targetDir))
        return
    if os.path.isfile(sourceDir):
        CopyFile(sourceDir, targetDir)
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or os.path.exists(targetFile) and os.path.getsize(targetFile) != os.path.getsize(sourceFile):
                targetFileHandle = open(targetFile, 'wb')
                sourceFileHandle = open(sourceFile, 'rb')
                targetFileHandle.write(sourceFileHandle.read())
                targetFileHandle.close()
                sourceFileHandle.close()
        if os.path.isdir(sourceFile):
            CopyFiles(sourceFile, targetFile)
            
def CopyFile(sourceFile, targetFile):
    sourceFile = Common.GetFullPath(sourceFile)
    targetFile = Common.GetFullPath(targetFile)
    if not os.path.exists(sourceFile):
        return
    if not os.path.exists(targetFile) or os.path.exists(targetFile) and os.path.getsize(targetFile) != os.path.getsize(sourceFile):
        targetDir = os.path.dirname(targetFile)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        targetFileHandle = open(targetFile, 'wb')
        sourceFileHandle = open(sourceFile, 'rb')
        targetFileHandle.write(sourceFileHandle.read())
        targetFileHandle.close()
        sourceFileHandle.close()
        
def GetUTF8Content(file):
    fileContent = open(file).read()
    for encoding in "utf-8-sig", "utf-16", "utf-8":
        try:
            return fileContent.decode(encoding)
        except UnicodeDecodeError:
            continue
    return fileContent.decode("latin-1")
        


def removeLineByKey(srcfile, keys, destfile):
    sfile = open(srcfile)
    lines = sfile.readlines()
    sfile.close()
    destfile = open(destfile, 'w')
    for line in lines:
        ismatch = False
        for key in keys:
            if re.search(r'^' + key, line):
                ismatch = True
                break
        if not ismatch:
            destfile.write(line)
    destfile.close()

def appendfile(srcfile, destfile):
    """append srcfile to destfile"""
    if not (os.path.exists(srcfile) and os.path.exists(destfile)):
        return
    srcContent = GetUTF8Content(srcfile)
    destContent = GetUTF8Content(destfile)
    dfile = open(destfile, 'w')
    dfile.write(destContent + '\n\n' + srcContent)
    dfile.close()

"""
merge srcfolder to destfolder, func is a function to process the 
situation of file have already exists
"""
def mergedir(srcfolder, destfolder, func = None, mode=True):
    if not os.path.exists(destfolder):
        os.makedirs(destfolder)
    if not os.path.exists(srcfolder):
        Common.Msg('%s does not exists')
        return

    srcfilelist = os.listdir(srcfolder)
    for file in srcfilelist:
        src = os.path.join(srcfolder, file)
        dest = os.path.join(destfolder, file)
        if os.path.isfile(src):
            if (not mergefile(src, destfolder, mode)) and (func != None):
                func(src, dest)
        else:
            mergedir(src, dest, func, mode)

"""
copy file to dir. srcfile and destfolder is fullpath. 
if file have already exists, when mode is Flase would
do nothin, otherwise would override.
"""
def mergefile(srcfile, destfolder, mode=True):
    destfilelist = os.listdir(destfolder)
    basename = os.path.basename(srcfile)
    if basename in destfilelist:
        # android/support 不处理
        if re.search(r'android.support', srcfile):
            return False
        if mode == True:
            Common.ErrorMsg('warning: %s already have the file %s, it will be override!' % 
                (destfolder, os.path.basename(srcfile)))
            shutil.copy(srcfile, destfolder)
            return True
        else:
            return False
    else:
        shutil.copy(srcfile, destfolder)
        return True

def findDex(folder):
    filelist = os.listdir(folder)
    for file in filelist:
        index = file.find('.dex')
        if (index > 0) and (index == len(file) - 4):
            dexPath = os.path.join(folder, file)
            return dexPath   

def findApk(folder):
    filelist = os.listdir(folder)
    for file in filelist:
        index = file.find('.apk')
        if (index > 0) and (index == len(file) - 4):
            dexPath = os.path.join(folder, file)
            return dexPath
def removeFile(srcfile):
    os.remove(srcfile)

def handlerTargetSdk(path):
    f = file(path)
    lines = f.readlines()
    f.close()
    num = 0
    minSdk = '8'
    targetSdk = '20'
    try:
        num = lines.index('sdkInfo:\n')
    except Exception,ex:
        print 'not sdkInfo:'
        sdkInfo = "sdkInfo:\n  minSdkVersion: '%s'\n  targetSdkVersion: '%s'\n" % (minSdk,targetSdk)
        lines.insert(6,sdkInfo)
        output = file(path, 'w')
        output.writelines(lines)
        output.close()
        return
    print num
    minSdkVersions = lines[num + 1]
    regex = '\d{1,}'
    if 'minSdkVersion' in minSdkVersions:
        result = re.search(regex,minSdkVersions)
        if result:
            print 'minSdk si '+result.group(0)
        #result = re.subn(regex, minSdk, minSdkVersions)
        #lines[num + 1] = result[0]
    else:
        minSdkVersion = "  minSdkVersion: '%s'\n" % (minSdk)
        lines.insert(num + 1,minSdkVersion)
    targetSdkVersions = lines[num + 2]
    if 'targetSdkVersion' in targetSdkVersions:
        result = re.subn(regex, targetSdk, targetSdkVersions)
        lines[num + 2] = result[0]
    else:
        targetSdkVersion = "  targetSdkVersion: '%s'\n" % (targetSdk)
        lines.insert(num + 2,targetSdkVersion)
    output = file(path, 'w')
    output.writelines(lines)
    output.close()
