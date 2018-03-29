# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re

import HandleIni

'''
将渠道的配置文件androidmanifest.xml复制到游戏的配置文件，并做相应修改
'''
class XmlHandle:
    # 游戏原有包名
    old_packname = ' '
    # 修改后的包名
    new_packname = ' '
    # 配置文件
    config_file = ' '
    # 应用名称
    app_name = ' '
    def __init__(self, configfile, srcfile, descfile):
        ET.register_namespace('android',r"http://schemas.android.com/apk/res/android")
        self.desc_file = descfile
        self.config_file = configfile
        self.src_tree = ET.parse(srcfile)
        self.src_root = self.src_tree.getroot()
        self.desc_tree = ET.parse(descfile)
        self.desc_root = self.desc_tree.getroot()
        self.old_packname = self.desc_root.get('package')
        self.new_packname = HandleIni.GetValueByKey(self.config_file, 'PACKAGE_NAME')
        self.app_name = HandleIni.GetValueByKey(self.config_file, 'GAME_NAME')
    # 处理包前缀标签
    def handlePackPrefix(self, ele):
        if ele.text is None:
            return
        desc_packname = self.desc_root.get('package')
        desc_packname = ele.text.strip()+desc_packname
        # self.new_packname  = desc_packname
        # self.desc_root.set('package', desc_packname)

    # 处理包后缀标签
    def handlePackSuffix(self, ele):
        if ele.text is None:
            return
        desc_packname = self.desc_root.get('package')
        desc_packname += ele.text.strip()
        # self.new_packname  = desc_packname
        # 在replacePackageName中充一更换包名
        # self.desc_root.set('package', desc_packname)

    # support-screens
    def handleSupport(self, ele):
        if ele.text is None:
            return
        desc_support_screens = self.desc_root.find('supports-screens')
        src_support_screens = ele.find('supports-screens')
        if src_support_screens is None:
            # 渠道配置文件有<sdk_support-screens>标签，却没有<supports-screens>
            raise Exception(r"channel androidmanifest.xml does not have <supports-screens> element!")
        if desc_support_screens is None:
            # 目标配置文件不存在该属性，直接添加即可
            self.desc_root.append(src_support_screens)
        else:
            # 如果已经存在，设置属性
            keys = src_support_screens.keys()
            for key in keys:
                desc_support_screens.set(key, src_support_screens.get(key))
    # 处理uses-sdk
    def handleuserSdk(self):
        userSdk = self.desc_root.find('uses-sdk')
        if userSdk:
            print 'has user sdk ele***************************************'
            userSdk.set('{http://schemas.android.com/apk/res/android}targetSdkVersion',19)
            userSdk.set('{http://schemas.android.com/apk/res/android}minSdkVersion',9)
        else:
            print 'has not user sdk ele***************************************'

    # 处理权限标签
    def handlePermission(self, ele):
        if ele.text is None:
            return
        all_permission = ele.findall('uses-permission')
        self.desc_root.extend(all_permission)
    
    # 将application的属性添加到目标配置文件中
    def handleApplication(self, ele):
        if ele.text is None:
            return
        app_ele = ele.find('application')
        if app_ele is None:
            return
        app_keys = app_ele.keys()
        desc_app_ele= self.desc_root.find('application')
        if desc_app_ele is None:
            raise Exception(r"destinated androidmanifest.xml does not have <application> element!")
        for key in app_keys:
            desc_app_ele.set(key, app_ele.get(key))

    ''' 处理其他标签，如activity,service,meta-tada。统一作为application标签
       的子标签复制进去'''    
    def handleOther(self, child):
        if child.text is None:
            return
        desc_app_ele= self.desc_root.find('application')
        if desc_app_ele is None:
            raise Exception(r"destinated androidmanifest.xml does not have <application> element!")
        for ele in child:
            if ele is not None:
                desc_app_ele.append(ele)
                
    # 处理需要替换的字段 by qingcui
    def handleReplace(self):
        """ $key$ replace by GetValueByKey(file, key) """
        file = open(self.desc_file, 'r')
        data = file.read()
        file.close()
        m = re.search(r'\$\w+\$', data)
        if not m:
            return
        all_args = re.findall(r'\$(\w+)\$', data)
        for match in all_args:        
            value = HandleIni.GetValueByKey(self.config_file, match)
            data = data.replace('$'+match+'$', value)
        file = open(self.desc_file, 'w')
        file.write(data)
        file.close()
    
    # 替换manifest中的包名 by qingcui
    def replacePackageName(self):
        if self.new_packname == '' or self.new_packname == None:
            print 'new_packname is null, no need to modify packagename of AndroidManifest.xml'
            return
        file = open(self.desc_file, 'r')
        content = file.read()
        file.close()
        content = content.replace(self.old_packname, self.new_packname,1)
        file = open(self.desc_file, 'w')
        file.write(content)
        file.close()

    # 替换游戏名称
    def replaceGameName(self):
        gameName = HandleIni.GetValueByKey(self.config_file, 'GAME_NAME')
        if not gameName:
            return
        application = self.desc_root.find('application')
        activitys = application.findall('activity')

        for activity in activitys:
            if self.isLaunchActivity(activity):
                activity.set('{http://schemas.android.com/apk/res/android}label', gameName)
                self.desc_tree.write(self.desc_file)
                return

    def isLaunchActivity(self, activity):
        for intentFilter in activity.findall('intent-filter'):
            for action in intentFilter.findall('action'):
                if action.get('{http://schemas.android.com/apk/res/android}name') != 'android.intent.action.MAIN':
                    continue
                for category in intentFilter.findall('category'):
                    if category.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.category.LAUNCHER':
                        return True
        return False

    # 根据主Acitivty修改其他Activity的屏幕方向
    def modefiedScreenOrientation(self):
        channel_id = HandleIni.GetValueByKey(self.config_file, 'GLOBAL_CHANNEL_ID')
        if channel_id == '10014':
            print '10014 channel not modefied ScreenOrientation********************'
            return
        else:
            screendir = HandleIni.GetValueByKey(self.config_file, 'GLOBAL_SCREENDIR')
            if screendir == '1':
                screendir = 'portrait'
                print 'screenOrientation:portrait ********************'+screendir
            else:
                screendir = 'landscape'
                print 'screenOrientation:landscape ********************'
            application = self.desc_root.find('application')
            activitys = application.findall('activity')
            for activity in activitys:
                activityScreenOrientation = activity.get('{http://schemas.android.com/apk/res/android}screenOrientation')
                
                if activity.get('{http://schemas.android.com/apk/res/android}screenOrientation'):
                    #print 'activity  screenOrientation ********************'+activityScreenOrientation
                    #如果有activity的方向不希望被修改可以在方向前面加一个$
                    if activityScreenOrientation.startswith('$'):
                        orientation = activityScreenOrientation.replace('$','')
                        activity.set('{http://schemas.android.com/apk/res/android}screenOrientation', orientation)
                        print 'has a activity keep screenOrientation ********************'+orientation
                    else:
                        activity.set('{http://schemas.android.com/apk/res/android}screenOrientation', screendir)
                self.desc_tree.write(self.desc_file)

    def replaceFieldName(self):
        file = open(self.desc_file, 'r')
        content = file.read()
        file.close()
        content = content.replace('${packagename}', self.new_packname)
        print 'replace qq qian bao packagename***************************************'
        file = open(self.desc_file, 'w')
        file.write(content)
        file.close()

    # 根据配置文件修改meta-data里面的值
    def modefiedMetadata(self):
        application = self.desc_root.find('application')
        metadatas = application.findall('meta-data')
        activitys = application.findall('activity')
        for metadata in metadatas:
            # 修改优酷渠道xml里面的配置参数
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'YKGAME_APPNAME':
                metadata.set('{http://schemas.android.com/apk/res/android}value', self.app_name)
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'YKGAME_APPID':
                appid = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_ID')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appid)
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'YKGAME_APPKEY':
                appkey = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_KEY')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appkey)
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'YKGAME_PRIVATEKEY':
                appsecret = HandleIni.GetValueByKey(self.config_file, 'APP_SECRET')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appsecret)
            # 修改联想渠道xml里面的配置参数
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'lenovo.open.appid':
                appid = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_ID')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appid)
            # 修改360渠道的meta-data
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'QHOPENSDK_APPID':
                appid = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_ID')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appid)
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'QHOPENSDK_APPKEY':
                appkey = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_KEY')
                metadata.set('{http://schemas.android.com/apk/res/android}value', appkey)
            if metadata.get('{http://schemas.android.com/apk/res/android}name') == 'QHOPENSDK_PRIVATEKEY':
                privatekey = HandleIni.GetValueByKey(self.config_file, 'APP_PRIVATEKEY')
                metadata.set('{http://schemas.android.com/apk/res/android}value', privatekey)
            self.desc_tree.write(self.desc_file)
        

        for activity in activitys:
            # 修改豌豆荚渠道xml里面的配置参数
            if activity.get('{http://schemas.android.com/apk/res/android}name') == 'com.wandoujia.oakenshield.activity.OakenshieldActivity':
                for intentFilter in activity.findall('intent-filter'):
                    for data in intentFilter.findall('data'):
                        if data.get('{http://schemas.android.com/apk/res/android}scheme'):
                            appid = HandleIni.GetValueByKey(self.config_file, 'ACCOUNT_APP_ID')
                            scheme = 'Wandoujia-PaySdk-' + appid
                            data.set('{http://schemas.android.com/apk/res/android}scheme',scheme)
                        self.desc_tree.write(self.desc_file)
            # 修改百度QQ钱包渠道xml里面的配置参数
            if activity.get('{http://schemas.android.com/apk/res/android}name') == 'com.baidu.platformsdk.pay.channel.qqwallet.QQPayActivity':
                for intentFilter in activity.findall('intent-filter'):
                    for data in intentFilter.findall('data'):
                        if data.get('{http://schemas.android.com/apk/res/android}scheme'):
                            scheme = 'qwallet' + self.new_packname
                            data.set('{http://schemas.android.com/apk/res/android}scheme',scheme)
                        self.desc_tree.write(self.desc_file)
            # 修改VIVO QQ钱包渠道xml里面的配置参数
            if activity.get('{http://schemas.android.com/apk/res/android}name') == 'com.bbk.payment.tenpay.VivoQQPayResultActivity':
                for intentFilter in activity.findall('intent-filter'):
                    for data in intentFilter.findall('data'):
                        if data.get('{http://schemas.android.com/apk/res/android}scheme'):
                            scheme = 'qwallet' + self.new_packname
                            data.set('{http://schemas.android.com/apk/res/android}scheme',scheme)
                        self.desc_tree.write(self.desc_file)

            
    '''调用该方法即可开始解析'''    
    def Handle(self):
        for child in self.src_root:
            if child.tag == 'pack_prefix':
                # self.handlePackPrefix(child)
                pass
            elif child.tag == 'pack_suffix':
                self.handlePackSuffix(child)
            elif child.tag == 'sdk_supports-screens':
                self.handleSupport(child)
            elif child.tag == 'sdk_uses-permission':
                self.handlePermission(child)
            elif child.tag == 'sdk_application':
                self.handleApplication(child)
            else :
                self.handleOther(child)
        # 完成后才输出修改
        self.replaceGameName()
        self.modefiedScreenOrientation()
        self.modefiedMetadata()
        self.handleuserSdk()
        self.desc_tree.write(self.desc_file, encoding="UTF-8", xml_declaration=True)

        self.handleReplace()
        self.replacePackageName()

