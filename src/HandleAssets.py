"""Handle Assets"""
import os

import HandleIni
import HandleFile
import Common

"""merge srcfolder to destfolder. they are fullpath."""
def mergeAssets(configfile ,srcfolder, destfolder):
    destIni = destfolder + '/DWSDKconfig.ini'
    HandleFile.mergedir(srcfolder, destfolder)
    HandleFile.CopyFile(configfile, destIni)

    removeKeys = ['GAME_NAME', 'PACKAGE_NAME', '#Packge message', 
        'KEYSTORE', 'KEYSTORE_PASSWORD', 'KEYALIAS', 'KEYALIAS_PASSWORD']
    HandleFile.removeLineByKey(configfile, removeKeys, destIni)
    needAppendFile = './config/DWSDKconfig.ini'
    if os.path.isfile(needAppendFile):
        HandleFile.appendfile(needAppendFile, destIni)
    HandleIni.encryIni(destIni)
