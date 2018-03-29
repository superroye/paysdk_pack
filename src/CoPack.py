# -*- coding: utf-8 -*-
#!/usr/bin/env python2.7
"""
Usage: gopack.py [flags] <input_apk_file> <game_folder> <output_apk_folder>
"""
import sys
import os

import Common
import HandleApk
import HandleIni
import HandleFile
import HandleXml
import HandleLibs
import HandleRes
import HandleSmali
import HandleAssets
import HandleRootFile
import HandleR
from HandleXml import XmlHandle
from Common import Tee

def PackOneSdk(input_apk_file, config_file, game_folder, output_folder):
    if os.path.isfile(input_apk_file) == False:
        Common.ErrorMsg("input apk file %s not exist" % input_apk_file)
        sys.exit(1)
    if os.path.isfile(config_file) == False:
        Common.ErrorMsg("config file %s not exist" % config_file)
        sys.exit(1)
    
    #解析config，获得渠道配置信息
    sdk = HandleIni.GetValueByKey(config_file, 'GLOBAL_CHANNEL_ID')
    Common.SetSdk(sdk)
    Common.SetConfigFile(config_file)

    outDir = Common.GetOutDir()
    tempDir = Common.GetTempDir()    
    workDir = Common.GetWorkDir()
    sdkDir = Common.GetSdkDir()
    
    gameName = HandleIni.GetValueByKey(config_file, 'GAME_NAME')
    version = HandleIni.GetValueByKey(sdkDir + 'assets/DWSDKinfo.ini', 'VERSION')
    if output_folder:
        output_file = output_folder + '/' + gameName + '-' + version + '-' + sdk + '.apk'
    else:
        output_file = outDir + sdk + '.apk'
    print '<a href=' + sdk + '></a>'
    print '%s channel is packing...' % sdk

    #合并混淆的映射文件mapping.txt
    mergeMappingFile(game_folder, output_folder, sdkDir)
    #预处理阶段：反编译apk    
    HandleApk.DecompileApk(input_apk_file, workDir)
    #patch AndroidManifest
    xml = XmlHandle(config_file, sdkDir + "AndroidManifest_channel.xml", workDir + 'AndroidManifest.xml')
    xml.Handle()
    #处理targetsdk
    HandleFile.handlerTargetSdk(workDir + 'apktool.yml')
    #patch asset
    HandleAssets.mergeAssets(config_file, sdkDir + 'assets', workDir + 'assets')
    #patch libs
    HandleLibs.mergeLibs(sdkDir + 'libs', workDir + 'lib')
    #patch res
    HandleRes.mergeRes(sdkDir + 'res', workDir + 'res', game_folder + '/icon/' + sdk)
    #patch smali 
    dexPath = HandleFile.findDex(sdkDir + 'out')
    HandleApk.DecompileDex(dexPath, tempDir + 'smali')

    HandleSmali.modifySmali(workDir + 'smali', xml.old_packname, xml.new_packname)
    HandleSmali.mergeSmali(tempDir + 'smali', workDir + 'smali',config_file)

    #处理微信支付相关的包名修改
    HandleSmali.modifyWXPackageName(workDir + 'smali', xml.new_packname)

    HandleR.CreateR(xml.new_packname)

    #后处理阶段：重新编译生成apk，对齐，签名
    HandleApk.CompileApk(workDir, tempDir + "out.apk")
    #处理root目录的文件资源
    HandleRootFile.copyRootFiles(tempDir + "out.apk",sdkDir)

    HandleApk.AlignApk(tempDir + "out.apk", tempDir + "out-aligned.apk")

    HandleApk.SignApk(tempDir + "out-aligned.apk")

    HandleFile.CopyFile(tempDir + "out-aligned.apk", output_file)
    print 'pack %s channel success ^_^\n\n' % sdk
    
def PackSdk(input_apk_file, game_folder, output_folder):
    if not (verifyFileParams(input_apk_file) and 
        verifyDirParams(game_folder) and 
        verifyDirParams(output_folder)):
        sys.exit(1)
    Common.SetOutDir(output_folder)
    Common.DelAllTempDir()
    cosdkConfigDir = game_folder + '/DWSDKconfig'
    configList = os.listdir(cosdkConfigDir)
    for configFile in configList:
        if not configFile.endswith('.ini'):
            Common.ErrorMsg('%s is not a ini file' % configFile)
            continue
        configFilePath = os.path.join(cosdkConfigDir, configFile)
        try:
            PackOneSdk(input_apk_file, configFilePath, game_folder, output_folder)
        except Exception as e:
            Common.ErrorMsg(e)

def PackSdk1(input_apk_file, game_folder, output_folder,channl_name):
    if not (verifyFileParams(input_apk_file) and 
        verifyDirParams(game_folder) and 
        verifyDirParams(output_folder)):
        sys.exit(1)
    Common.SetOutDir(output_folder)
    Common.DelAllTempDir()
    cosdkConfigDir = game_folder + '/DWSDKconfig'
    configList = os.listdir(cosdkConfigDir)
    for configFile in configList:
        if not configFile.endswith('.ini'):
            Common.ErrorMsg('%s is not a ini file' % configFile)
            continue
        configName = channl_name + '.ini'
        if configFile == configName:
            Common.ErrorMsg('%s is a pacage file' % configFile)
            configFilePath = os.path.join(cosdkConfigDir, configFile)
            try:
                PackOneSdk(input_apk_file, configFilePath, game_folder, output_folder)
            except Exception as e:
                Common.ErrorMsg(e)
            break;

def verifyFileParams(filepath):
    if filepath == None or filepath == "":
        Common.ErrorMsg("Input parameters error, can't be null!")
        return False
    if not os.path.isfile(filepath):
        Common.ErrorMsg('Input parameters error, %s is not a file!!' % filepath)
        return False
    return True

def verifyDirParams(dirpath):
    if dirpath == None or dirpath == "":
        Common.ErrorMsg("Input parameters error, can't be null!")
        return False
    if not os.path.isdir(dirpath):
        Common.ErrorMsg('Input parameters error, %s is not a directory!!' % dirpath)
        return False
    return True  

def mergeMappingFile(game_folder, output_folder, sdkDir):
    mapfilename = '/mapping.txt'
    gameMapping = game_folder + mapfilename
    if not verifyFileParams(gameMapping):
        print "game folder don't exits mappting.txt. Would not merge mappting file"
        return
    outMapping = output_folder + mapfilename
    channelMapping = sdkDir + mapfilename
    cosdkMapping = Common.GetConfigDir() + mapfilename
    HandleFile.CopyFile(gameMapping, outMapping)
    HandleFile.appendfile(cosdkMapping, outMapping)
    HandleFile.appendfile(channelMapping, outMapping)

def goPack(argv):
    reload(sys) 
    sys.setdefaultencoding('utf8')     
    
    path = os.environ.get('PATH')
    if Common.GetSystem() == 'Windows':
        path = path + './tools/windows;'
    elif Common.GetSystem() == 'Linux':
        path = path + './tools/linux;'
    elif Common.GetSystem() == 'Mac':
        path = path + './tools/mac;'
    os.putenv('PATH', path)
    print 'The System is ', Common.GetSystem()

    # Common.curDir = sys.path[0]
    Common.curDir = '.'

    if argv[1].startswith('-'):
        Common.flag = argv[1]
        params = argv[2:]
    else:
        params = argv[1:]
    if len(params) == 3:
        PackSdk(params[0], params[1], params[2])
    elif len(params) == 4:
        PackSdk1(params[0], params[1], params[2],params[3])
    else:
        Common.Usage(argv[0] + "[flags] <input_apk_file> <game_folder> <output_apk_folder>")
        sys.exit(1)
        
if __name__ == '__main__':
    try:
    	sys.stdout = Tee()
        goPack(sys.argv)
    except RuntimeError, e:
        print "ERROR : %s" % (e,)
        sys.exit(1)
