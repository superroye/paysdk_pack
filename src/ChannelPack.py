import os
import Common
import shutil
import Config

workPath = ""
def channelPack(name):

    channeldir = Config.getSrcPath() + name
    outdir = channeldir+"/out"

    if(os.path.exists(outdir)):
        shutil.rmtree(outdir)

    createDir(name)
    copyRes(name)

    javaSrcdir = Config.getSrcPath() + name + "/src/main/java"

    global workPath
    workPath = os.getcwd()
    os.chdir('../')
    androidPath = os.getcwd()+"/tools/android.jar"
    sdklib = Config.getOutPath()+"XLSdkLib/libs/*"

    os.chdir(channeldir)
    jarlibsPath = os.getcwd()+"/libs/*"

    classesPath = outdir + '/classes'
    os.makedirs(classesPath)
    os.chdir(channeldir)

    savaPathToTxt(outdir,javaSrcdir)

    cmdclass = 'javac -source 1.7 -target 1.7 -encoding "utf-8" -d %s @%s -classpath %s;%s;%s;' % (classesPath,outdir+"/sources.txt", androidPath, jarlibsPath, sdklib)
    print cmdclass
    Common.ExecuteCmd(cmdclass)
    cpath = os.getcwd()
    os.chdir(classesPath)
    cmdJar = 'jar cvf "%s".jar ./' % (name)
    print cmdJar
    Common.ExecuteCmd(cmdJar)
    print cpath
    os.chdir(cpath)

    copyJars(name)
    createDex(name)

def savaPathToTxt(outdir,srcpath):
    sf = open(outdir+"/sources.txt", "w")
    savePath(sf, srcpath)
    sf.close()

def savePath(file, filepath):
    if os.path.isdir(filepath):
        list = os.listdir(filepath)
        for file1 in list:
            savePath(file, os.path.join(filepath, file1))
    else:
        file.write(filepath+"\n")

def createDir(name):
    channeldir = Config.getSrcPath() + name
    outdir = channeldir+"/out/plugin"
    libs = outdir+"/libs"
    res = outdir + "/res"
    assets = outdir + "/assets"
    os.makedirs(libs)
    os.makedirs(res)
    os.makedirs(assets)

def copyRes(name):
    channeldir = Config.getSrcPath() + name
    outdir = channeldir+"/out/plugin"
    Common.copyFiles(channeldir+"/src/main/assets",outdir + "/assets")
    Common.copyFiles(channeldir + "/src/main/res", outdir + "/res")
    Common.copyFiles(channeldir + "/src/main/AndroidManifest.xml", outdir)

def copyJars(name):
    print "copy jars..."
    base = Config.getSrcPath() + name
    libs = base + "/libs"
    jars = base +"/out/jar"
    os.mkdir(jars)
    shutil.copy(base+"/out/classes/"+name+".jar" , jars)
    if os.path.exists(libs):
        list = os.listdir(libs)
        for file in list:
            if file.endswith(".jar"):
                print("jar: " + libs + "/" + file)
                shutil.copy(libs + "/" + file, jars)
            else:
                other = base + "/out/plugin/libs/"+file
                os.mkdir(other)
                print("so: " + libs + "/" + file)
                list1 = os.listdir(libs + "/" + file)
                for file1 in list1:
                    shutil.copy(libs + "/" + file + "/" + file1, other)



def createDex(name):
    os.chdir(workPath)
    dx = "../tools/common/dx.jar"

    base = Config.getSrcPath() + name
    outdir = base + "/out/plugin"
    outPath = outdir + "/" + name + ".dex"
    inPath = base +"/out/jar/"
    cmdDex = 'java -jar "%s" --dex --output="%s" "%s"' % (dx, outPath, inPath)
    print cmdDex
    Common.ExecuteCmd(cmdDex)

channelPack("m4399lib")