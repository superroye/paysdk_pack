# -*- coding: utf-8 -*-
"""merge res"""
import os
import re
import shutil
import xml.etree.ElementTree as ET
import fnmatch
import HandleFile
import Common

def mergeRes(srcfolder, destfolder, iconfolder):
    #modifyV4ResDirName(destfolder) # <<<modify by Roye
	#removeDuowanRes(destfolder) #<<<modify by Roye
    HandleFile.mergedir(srcfolder, destfolder, processExistsFile, False) 
    # remove duowan channel res
    removeDummyRes(destfolder)
    #replace icon
    HandleFile.mergedir(iconfolder, destfolder, processExistsIcon)

def processExistsFile(srcfile, destfile):
    if re.search(r'res.*values', srcfile):
        mergeValuesXml(srcfile, destfile)
    else:
        Common.ErrorMsg('warning: %s already have the file %s, it will be override!' % 
                (os.path.dirname(destfile), os.path.basename(srcfile)))
        shutil.copy(srcfile, destfile)

def processExistsIcon(srcfile, destfile):
    shutil.copy(srcfile, destfile)

def mergeValuesXml(srcfile, destfile):
    srctree = ET.parse(srcfile)
    desttree = ET.parse(destfile)
    srcroot = srctree.getroot()
    destroot = desttree.getroot()
    if not isequale(srcroot, destroot):
        Common.ErrorMsg('merge %s failed. the root tag is not same!'% srcfile)
    else:
        for child in srcroot:
            if iscontain(child, destroot):
                Common.ErrorMsg('%s child tag "%s" conflict'%
                    (srcfile, child.attrib))
            else:
                destroot.append(child)
        desttree.write(destfile)

"""if srcele equale destele return True, otherwise return False
   if attriblist isn't None, only check the attri in the
   attriblist.
"""
def isequale(srcele, destele, attriblist = None):
    srcdict = srcele.attrib
    destdict = destele.attrib
    if srcele.tag != destele.tag:
        return False
    if attriblist:
        for k in attriblist:
            if srcdict.get(k) != destdict.get(k):
                return False
    else:
        if len(srcdict) != len(destdict):
            return False
        for k, v in srcdict.items():
            if v != destdict.get(k):
                return False
    return True

"""if ele is the child of parentele, return true"""
def iscontain(ele, parentele):
    for child in parentele:
        if isequale(ele, child):
            return True
    return False

def filterDummy(name):
    regex = 'name=\"dummy_'
    if regex in name:
        print 'delete:'+name
        return False
    else:
        return True

def handlerDummyRes(path):
    f = file(path)
    lines = f.readlines()
    lines = filter(filterDummy,lines)
    output = file(path, 'w')
    output.writelines(lines)
    output.close()

#must remove res/values/public.xml
def removeDummyRes(destfolder):
    basedir = destfolder
    for file in os.listdir(basedir):
        listfiles = os.listdir(os.path.join(basedir,file))
        for file1 in listfiles:
            if fnmatch.fnmatch(file1, 'dummy_*'):
                print 'delete ' + file1
                os.remove(os.path.join(basedir, file, file1))
    handlerDummyRes(destfolder+os.sep+'values'+os.sep+'public.xml')

def modifyV4ResDirName(destfolder):
    basedir = destfolder
    for file in os.listdir(basedir):
        if fnmatch.fnmatch(file, '*-v4'):
            os.rename(os.path.join(basedir, file),os.path.join(basedir, file.replace('-v4','',1)))
