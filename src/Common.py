# -*- coding: utf-8 -*-
"""
Usage: gopack.py [flags] <input_apk_file> <game_folder> <output_apk_folder>
"""
import re
import sysconfig
import platform
import shutil
import subprocess
import inspect
import os

class Tee(object):
    def __init__(self):
        self.file = open("CoPack.log", "w+")
        self.stdout = sysconfig.stdout
    def __del__(self):
        sysconfig.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
        
curDir = '.'
flag = ''
configFile = ''
sdk = ''
outDir = ''

def Usage(usage):
    print (usage)

def Msg(msg):
    global flag
    if flag == '-v':
        print (msg)

def ErrorMsg(msg):
    print (msg)
    
def ErrorMsgThrowException(msg):
    print (msg)
    raise Exception('Execute Command Error')

def ErrorMsgAndExit(msg, ret=1):
    print (msg)
    exit(ret) 
    
def ExecuteCmd(cmd):
    cmd = cmd.replace('\\', '/')
    cmd = re.sub('/+', '/', cmd)
    if platform.system() == 'Windows':
        st = subprocess.STARTUPINFO
        st.dwFlags = subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow = subprocess.SW_HIDE
        cmd = str(cmd).encode('gbk')
    print (cmd)
    s = subprocess.Popen(cmd, shell=True)
    ret = s.wait()

    if ret:
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdoutput, erroutput = s.communicate()
        cmd = 'ERROR:' + cmd + ' ===>>> exec Fail <<<=== '
        ErrorMsgThrowException(cmd)
    else:
        cmd += ' ===>>> exec success <<<=== '
        Msg(cmd)
    return ret

def GetSystem():
    system = 'Windows'
    if sysconfig.platform.startswith('win'):
        system = 'Windows'
    elif sysconfig.platform.startswith('linux'):
        system = 'Linux'
    elif sysconfig.platform.startswith('darwin'):
        system = 'Mac'
    return system

def GetCurDir():
    global curDir
    retPath = curDir
    if platform.system() == 'Windows':
        retPath = retPath.decode('gbk')
    return retPath
    caller_file = inspect.stack()[0][1]
    retPath = os.path.abspath(os.path.dirname(caller_file))
    if platform.system() == 'Windows':
        retPath = retPath.decode('gbk')
    return retPath

def GetFullPath(filename):
    if os.path.isabs(filename):
        return filename
    dirname = GetCurDir()
    filename = os.path.join(dirname, filename)
    filename = filename.replace('\\', '/')
    filename = re.sub('/+', '/', filename)
    return filename

def GetToolsDir():
    if GetSystem() == 'Windows':
        return GetCurDir() + "/tools/windows/"
    elif  GetSystem() == 'Linux':
        return GetCurDir() + "/tools/linux/"
    elif  GetSystem() == 'Mac':
        return GetCurDir() + "/tools/mac/"
    else:
        return GetCurDir() + "/tools/windows/"

def GetCommonToolsDir():
    return GetCurDir() + "/tools/common/"

def GetConfigDir():
    return GetCurDir() + "/config/"

def GetCOSDKConfigDir():
    return GetConfigDir() + "DWSDKconfig/"

def SetOutDir(outfolder):
    global outDir
    outDir = outfolder

def GetOutDir():
    global outDir
    return outDir + ''
    
def GetWorkDir():
    game = GetTempDir() + "game/"
    if not os.path.exists(game):
        os.makedirs(game)
    return game

def GetTempDir():
    global sdk
    temp = GetOutDir() + "temp/" + sdk + '/'
    if not os.path.exists(temp):
        os.makedirs(temp)
    return temp

def DelAllTempDir():
    temp = GetOutDir() + "temp/"
    if os.path.exists(temp):
        shutil.rmtree(temp)

def GetSdkDir():
    global sdk
    return GetConfigDir() + sdk + '/'

def SetSdk(channelCode):
    global sdk
    sdk = channelCode

def SetConfigFile(configfile):
    global configFile
    configFile = configfile;

def GetConfigFile():
    global configFile
    return configFile

def copyFiles(srcpath, targetPath):
    if os.path.exists(srcpath):
        print("copyFiles: " + srcpath)
        if os.path.isdir(srcpath):

            print("copyFiles : " + srcpath)
            if os.path.exists(targetPath) == False:
				os.mkdir(targetPath)
            list = os.listdir(srcpath)
            for file in list:
                file1 = os.path.join(srcpath, file)
                subdir = targetPath
                if(os.path.isdir(file1)):
					subdir=os.path.join(targetPath, file)
                copyFiles(file1, subdir)
        else:
            os.path.isfile(srcpath)
            print("copyFiles : " + srcpath)
            shutil.copy(srcpath, targetPath)
