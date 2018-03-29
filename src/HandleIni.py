# -*- coding: utf-8 -*-
"""
"""
import ConfigParser
import StringIO
import os
import re

import HandleFile
import Common

def UpdateValueByKey(file, key, value):
    fileContent = '[global]\n' + HandleFile.GetUTF8Content(file)
    dummyFp = StringIO.StringIO(fileContent)
    dummyFp.seek(0, os.SEEK_SET)
    config = ConfigParser.RawConfigParser(allow_no_value = True)
    config.optionxform = str
    config.readfp(dummyFp)
    config.set('global', key, value)
    with open(file, 'wb') as configFile:
        config.write(configFile)
    with open(file, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(file, 'w') as fout:
        fout.writelines(data[1:])

def GetValueByKey(file, key):
    fileContent = '[global]\n' + HandleFile.GetUTF8Content(file)
    dummyFp = StringIO.StringIO(fileContent)
    dummyFp.seek(0, os.SEEK_SET)
    config = ConfigParser.RawConfigParser(allow_no_value = True)
    config.readfp(dummyFp)
    value = None
    try:
        value = config.get('global', key)
    except:
        print '%s has no key of %s' % (file, key)
    finally:
        return value
        
def UpdateValueByKey2(file, key, value):
    with open(file, "r") as source:
        lines = source.readlines()
    with open(file, "wb") as source:
        for line in lines:
            source.write (re.sub(r'^'+ key, key + '=' + value, line))

def removeValueByKey(file, dest, key):
    destfile = open(dest, 'w')
    fileContent = '[global]\n' + open(file).read()
    dummyFp = StringIO.StringIO(fileContent)
    dummyFp.seek(0, os.SEEK_SET)
    config = ConfigParser.RawConfigParser(allow_no_value = True)
    config.readfp(dummyFp)
    config.remove_option('global', key)
    config.write(destfile)

def encryIni(srcfile):
    secret = 'B19F67249DDF4675'
    encryTool = Common.GetCommonToolsDir() + 'encodeIni.jar'
    cmd = 'java -jar %s %s %s' % (encryTool, secret, srcfile)
    Common.ExecuteCmd(cmd)
