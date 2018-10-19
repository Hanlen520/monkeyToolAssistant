#!usr/bin/env python
# -*- coding:utf-8 _*-
import os
import re


def get_error_time(filepath):
    path = os.path.dirname(filepath)
    filebasename = os.path.basename(filepath).strip("Errorlist.txt")
    error_count = path + os.sep + filebasename + "Errorcount.txt"
    print("error_count =" + str(error_count))
    print("path = " + str(path))
    if os.path.exists(error_count):
        os.remove(error_count)
    else:
        pass
    errorCount = open(error_count, 'a+')
    reader = open(filepath, 'r')
    line = reader.readline()
    # errorname：times
    tmp = {}
    while not line == '':
        res = line.strip().split("// ")[1]
        str_error = re.sub(u"\\(.*?\\)", "", res.strip().strip("// ")).strip()
        print(str(str_error))
        if str_error in tmp.keys():
            tmp[str_error] = tmp[str_error] + 1
        else:
            tmp[str_error] = 1
        line = reader.readline()
    # print tmp
    for key in tmp.keys():
        print("key = "+key)
        errorCount.writelines(key + '=' + str(tmp[key]) + '\n')
    errorCount.close()

    if tmp:
        return True
    else:
        return False


if __name__ == '__main__':
    path = os.getcwd() + os.sep
    print("path =" + path)
    files = os.listdir(path)
    for file in files:
        if file.endswith('.txt'):
            if not file.endswith('Errorcount.txt'):
                print("file_path = "+path+file)
                get_error_time(path+file)
