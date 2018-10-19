#!usr/bin/env python3
# -*- coding:utf-8 _*-
"""
    @author:wangzhen
    @contact: zhen.wang@ontim.cn
    @file: monkeyExcutor.py
    @time: 2018-10-11
    @desc: Analyses monkeyLog and pull all logs
    """
import os
import threading


class GetDutInfo():

    def checkappinstalled(pack) -> bool:
        os.system("adb shell pm -l >app.txt")
        appfile = 'app.txt'
        flag = False
        for i in range(len(pack)):
            print(str(i) + " : " + pack[i])
        file_object = ''
        try:
            file_object = open(appfile)
            file_context = file_object.readline().strip()
            while not file_context == "":

                if pack == file_context.split(':')[1].strip():
                    flag = True
                    break
                file_context = file_object.readline().strip()

        finally:
            file_object.close()
            os.remove(appfile)
        return flag


class MonkeyExcutorThread(threading.Thread):

    def __init__(self, phone_tag, package, white_list, black_list):
        threading.Thread.__init__(self)
        self.phone_tag = phone_tag
        self.package = package
        self.white_list = white_list
        self.black_list = black_list

    def run(self):
        if not self.package == "":
            if GetDutInfo.checkappinstalled(self.package):
                pass
            else:
                print("the Apk is not installed")
        else:
            if not self.white_list == '' and self.black_list == '':
                # 带白名单的monkey测试
                pass
            elif not self.black_list == '' and self.white_list == '':
                # 带黑名单的monkey测试
                pass
            elif self.black_list == '' and self.white_list == '':
                # 整机monkey测试
                pass
            else:
                print("both black and white list exists is not allowed")