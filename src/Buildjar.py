import zipfile
import os
import Common
import shutil
import Config

workPath = ""

def initPath():
    global workPath
    workPath = os.getcwd()
    workPath = workPath.replace("\\","/")
    os.chdir(workPath)

def buildJar():
    initPath()
    srcPath = Config.getSrcPath()
    if os.path.exists(workPath+"/out"):
        shutil.rmtree(workPath+"/out")
    copyXLsdklib(srcPath+"paycommonlib","XLSdkLib", "paycommonlib")
    copyXLsdklib(srcPath+"paysdk", "XLSdkLib", "paysdk")
    copyXLsdklib(srcPath+"mipaylib", "xiaomiPlugin", "xiaomiPlugin")

def copyXLsdklib(projPath, projName, projJar):
    os.chdir(workPath)

    your_delet_file = "BuildConfig.class"
    zip = projPath+"/build/intermediates/bundles/release/classes.jar"
    outclasses = "./out/"+projName+"/classes"
    if os.path.exists(outclasses):
        shutil.rmtree(outclasses)

    zin = zipfile.ZipFile(zip)
    zin.extractall(outclasses)
    zin.close()

    deleteFile(outclasses, your_delet_file)
    reBuildJar(outclasses, projJar)
    copyBuildJar(projName, projJar)

def deleteFile(filepath,filename):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if os.path.isdir(child):
            deleteFile(child,filename)
        elif child.endswith(filename):
            print(child)
            os.remove(child)
            break


def reBuildJar(classesPath,jarName):
    print(classesPath)
    os.chdir(classesPath)
    cmdJar = 'jar cvf %s.jar ./' % (jarName)
    print (cmdJar)
    Common.ExecuteCmd(cmdJar)

def copyBuildJar(projName, projJar):
    src = workPath+"/out/"+projName+"/classes/"+projJar+".jar"
    target = Config.getOutPath()+projName+"/libs"
    shutil.copy(src, target)


