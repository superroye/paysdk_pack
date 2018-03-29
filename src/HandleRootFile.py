#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
import os
import Common


def list_files(src, resFiles, igoreFiles):
 
    if os.path.exists(src):
        if os.path.isfile(src) and src not in igoreFiles:
            resFiles.append(src)
        elif os.path.isdir(src):
            for f in os.listdir(src):
                if src not in igoreFiles:
                    list_files(os.path.join(src, f), resFiles, igoreFiles)
 
    return resFiles

def copyRootFiles(apkfilePath,decompileDirPath):
    print '%s copyRootFiles... %s' % (decompileDirPath,apkfilePath)
    addFiles = []
    igoreFiles = ['AndroidManifest_channel.xml','res','libs','out','assets']
    igoreFileFullPaths = []
    for ifile in igoreFiles:
        fullpath = os.path.join(decompileDirPath, ifile)
        igoreFileFullPaths.append(fullpath)
    addFiles = list_files(decompileDirPath, addFiles, igoreFileFullPaths)
    if len(addFiles) <= 0:
        print 'copyRootFiles is null...'
        return
    
    apkfile = os.path.abspath(apkfilePath)
    aapt = os.path.abspath(Common.GetToolsDir() + "aapt")
    decompileDir = decompileDirPath	
       
    addCmd = '"%s" a "%s"'
    for f in addFiles:
        fname = f[(len(decompileDir)):]
        addCmd = addCmd + ' ' + fname
    addCmd = addCmd % (aapt, apkfile)

    currPath = os.getcwd()

    os.chdir(decompileDirPath)
    Common.ExecuteCmd(addCmd)
    os.chdir(currPath)