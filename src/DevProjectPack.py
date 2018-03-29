#coding:utf-8
import Buildjar
import Copy
import Config
import HandleGradle

#游戏对接工程打包
def toPack():
    # print(Config.getSrcPath())
    # print(Config.getOutPath())

    Copy.makeRoot()
    Copy.makeLibDir("paysdk", "XLSdkLib")
    Copy.makeLibDir("paycommonlib", "XLSdkLib")
    Copy.makeLibDir("mipaylib", "xiaomiPlugin")
    Copy.makeSDKDemo("app","XLSDKDemo")

    Buildjar.buildJar()

    HandleGradle.handleDemo(Config.getOutPath()+"/XLSDKDemo/build.gradle")
    HandleGradle.handleXLSDK(Config.getOutPath()+"/XLSdkLib/build.gradle")
    HandleGradle.handlePlugin(Config.getOutPath()+"/xiaomiPlugin/build.gradle")
    HandleGradle.createRootNeedGradles()


toPack()
