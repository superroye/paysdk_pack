# -*- coding: utf-8 -*-
"""modified R for channel sdk"""

import os
import Common

def CreateR(packageName):
    packagepath = packageName.replace('.', '/')
    workDir    = Common.GetWorkDir()
    outRdir    = Common.GetTempDir()
    aaptTool   = Common.GetToolsDir() + "aapt"
    androidjar = Common.GetCommonToolsDir() + "android.jar"
    cmdR = '"%s" package -f -m -J "%s" -S "%s"res -I "%s" -M "%s"AndroidManifest.xml' % (aaptTool,outRdir,workDir,androidjar,workDir)
    print cmdR
    Common.ExecuteCmd(cmdR)
    CreateRClass(outRdir,packagepath)

def CreateRClass(outRdir,packagepath):
    jarName = 'R'
    rpath = outRdir + packagepath
    classesPath = outRdir+'classes'
    os.makedirs(classesPath)
    cmdRclass = 'javac -d "%s" "%s"/"%s".java -source 1.7 -target 1.7 -encoding UTF-8' % (classesPath,rpath,jarName)
    print cmdRclass
    Common.ExecuteCmd(cmdRclass)
    cpath = os.getcwd()
    os.chdir(classesPath)
    cmdJar = 'jar cvf "%s".jar ./' % (jarName)
    print cmdJar
    Common.ExecuteCmd(cmdJar)
    print cpath
    os.chdir(cpath)
    CreateRDex(classesPath,jarName)

def CreateRDex(outRdir,jarName):
    dx = Common.GetCommonToolsDir() + "dx.jar"  
    outPath = outRdir+"/"+jarName+".dex"
    inPath = outRdir+"/"+jarName+".jar"
    cmdDex = 'java -jar "%s" --dex --output="%s" "%s"' % (dx,outPath,inPath)
    print cmdDex
    Common.ExecuteCmd(cmdDex)
    CreateRSmali(outRdir,jarName)

def CreateRSmali(outRdir,jarName):
    outPath    = Common.GetWorkDir()+"smali"
    dexPath = outRdir+"/"+jarName+".dex"
    baksmali = Common.GetCommonToolsDir() + "baksmali-2.0.5.jar"
    cmdSmali ='java -jar "%s" -o "%s" "%s"' % (baksmali,outPath,dexPath)
    print cmdSmali
    Common.ExecuteCmd(cmdSmali)