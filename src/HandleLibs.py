"""merge libs"""
import os

import HandleFile
import Common
import HandleIni
"""merge srcfolder to destfolder. they are fullpath."""
def mergeLibs(srcfolder, destfolder):
    HandleFile.mergedir(srcfolder, destfolder, processExistsFile)

def processExistsFile(srcfile, destfile):
    Common.ErrorMsg('error: %s already have the file %s'%
                    (os.path.dirname(destfile), os.path.basename(srcfile)))

