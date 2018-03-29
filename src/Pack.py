
import Buildjar
import Copy
import Config
import HandleApk

def toPack(apkPath, plugin):
    HandleApk.DecompileApk(apkPath, plugin)
    print "pack plugin apk"

toPack("D:\\work_test\\demo.apk","D:\\work_test\\temp")




