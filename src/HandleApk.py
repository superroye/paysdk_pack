# -*- coding: utf-8 -*-
"""
"""
import os
import Common
import HandleIni

def GetApkTool():
    return Common.GetCommonToolsDir() + "apktool_2.3.1.jar"
    #return Common.GetCommonToolsDir() + "apktool_2.0.0rc2.jar"
    #return Common.GetCommonToolsDir() + "apktool_2.0.0rc3.jar"

def GetBakSmaliTool():
    return Common.GetCommonToolsDir() + "baksmali-2.0.5.jar"
    #return Common.GetToolsDir() + "baksmali-1.4.1.jar"

def GetAapt():
    return Common.GetToolsDir() + "aapt"

def GetZipAlign():
    return Common.GetToolsDir() + "zipalign"

def GetSignJarTool():
    return "jarsigner"

def GetKeyStoreInfo():
    keyStore = Common.GetConfigDir()+ "crack.keystore"
    storePassword = "787878"
    keyAlias = "crack"
    aliasPassword = "787878"
    print "============="+keyStore
    # config = Common.GetConfigFile()
    # keyStore = HandleIni.GetValueByKey(config, 'KEYSTORE')
    # storePassword = HandleIni.GetValueByKey(config, 'KEYSTORE_PASSWORD')
    # keyAlias = HandleIni.GetValueByKey(config, 'KEYALIAS')
    # aliasPassword = HandleIni.GetValueByKey(config, 'KEYALIAS_PASSWORD')
    return keyStore, storePassword, keyAlias, aliasPassword

def DecompileApk(apkFile, outDir):
    apkTool = GetApkTool()
    if Common.GetSystem() == "Linux":
        decompileApkCmd = 'java -jar "%s" -q d --frame-path "%s" -f "%s" -o "%s"' % (apkTool, Common.GetCommonToolsDir() + 'apktool', apkFile, outDir)
    else:
        decompileApkCmd = 'java -jar "%s" -q d -f "%s" -o "%s"' % (apkTool, apkFile, outDir)
    #decompileApkCmd = 'java -jar "%s" -q d -f "%s" "%s"' % (apkTool, apkFile, outDir)
    Common.ExecuteCmd(decompileApkCmd)
    
def CompileApk(inDir, apkFile):
    apkTool = GetApkTool()
    if Common.GetSystem() == "Linux":
        compileApkCmd = 'java -jar "%s" -q b --frame-path "%s" -f "%s" -o "%s"' % (apkTool, Common.GetCommonToolsDir() + 'apktool', inDir, apkFile)
    else:
        compileApkCmd = 'java -jar "%s" -q b -f "%s" -o "%s"' % (apkTool, inDir, apkFile)
    #decompileApkCmd = 'java -jar "%s" -q d -f "%s" "%s"' % (apkTool, apkFile, outDir)
    Common.ExecuteCmd(compileApkCmd)
    
def AlignApk(inApkFile, outApkFile):
    alignTool = GetZipAlign()
    alignCmd = '"%s" -f 4 "%s" "%s"' % (alignTool, inApkFile, outApkFile)
    Common.ExecuteCmd(alignCmd)
    
def SignApk(apkFile):    
    aapt = GetAapt()
    signJar = GetSignJarTool()
    keyStore, storePassword, keyAlias, aliasPassword = GetKeyStoreInfo()
    if not os.path.exists(keyStore):
        return 0
            
    listcmd = '%s list %s' % (aapt, apkFile)
    listcmd = listcmd.encode('gb2312')
    output = os.popen(listcmd).read()
    for filename in output.split('\n'):
        if filename.find('META-INF') == 0:
            removeMetaCmd = '"%s" remove "%s" "%s"' % (aapt, apkFile, filename)
            Common.ExecuteCmd(removeMetaCmd)
            
    signApkCmd = '"%s" -keystore "%s" -storepass "%s" -keypass "%s" "%s" "%s" -sigalg SHA1withRSA -digestalg SHA1' % (
                  signJar,
                  keyStore,
                  storePassword,
                  aliasPassword,
                  apkFile,
                  keyAlias)
    ret = Common.ExecuteCmd(signApkCmd)
    
    return ret

def DecompileDex(dexFile, outDir):
    bakSmaliTool = GetBakSmaliTool()
    
    decomplieJarCmd = 'java -jar "%s" -o "%s" "%s"' % (bakSmaliTool, outDir, dexFile)
    ret = Common.ExecuteCmd(decomplieJarCmd)
    return ret