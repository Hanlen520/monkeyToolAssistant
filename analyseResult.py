#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
    @author:wangzhen
    @contact: zhen.wang@ontim.cn
    @file: analyseResult.py
    @time: 2018-07-06
    @desc: Analyses monkeyLog and pull all logs
    """

# 获取所有的连接手机的sn
import os
import re
import time


def get_sn():
    sns = []
    cmd = os.popen("adb devices")
    line = cmd.readline()
    while not line == "":

        content = str(line)
        if content.startswith("List"):
            line = cmd.readline().strip()
            continue
        else:
            if "device" in line:
                status = content.split('\t')[1]
                sn = content.split('\t')[0]
                # print(status)
                if status == 'device':
                    sns.append(sn)
        line = cmd.readline().strip()
    return sns


def get_phone_tag(sn):
    path = '/data/local/tmp/'
    files = os.popen('adb -s %s shell ls %s' % (sn, path))
    read = files.readline().strip()
    tag = ""
    if not read == '':
        con = str(read)
        if '_' in con:
            tag = con.split('_')[1].strip('.log')
        else:
            tag = sn[-6::]
        print(tag)

    else:
        print('No log found')
    return tag


def get_monkey_log(sn, pathlocal):
    path = '/data/local/tmp'
    files = os.popen('adb -s %s shell ls %s' % (sn, path))
    read = files.readline()
    os.system("adb -s %s remount" % sn)
    if not read == '':
        con = str(read).strip()
        if '.log' in con:
            os.system("adb -s %s pull %s %s" % (sn, path + os.sep + con, pathlocal + os.sep + con))
            return pathlocal + os.sep + con
        else:
            return pathlocal + os.sep + sn[-6::]


def timeShift(time):
    h = int(time / 3600000)
    m = int((time / 60000 - h * 60))
    s = int((time / 1000 - h * 3600 - m * 60))
    return h, m, s


def analysisMonkeylog(logfile):
    haserror = False
    if os.path.exists(logfile):
        print('Analysing Results...')
        start = 0
        end = 0
        file_path = os.path.dirname(logfile) + os.sep
        file_name = os.path.split(logfile)[-1]
        curfol = os.path.join(file_path, file_name.strip('.log'))
        timeTagfile = curfol + '_Timetag.txt'
        errorfile = curfol + '_Errorlist.txt'
        if os.path.exists(timeTagfile):
            os.remove(timeTagfile)
        if os.path.exists(errorfile):
            os.remove(errorfile)
        timeTagTxt = open(timeTagfile, 'a+')
        errorTxt = open(errorfile, 'a+')
        # print("files=" + tmp_path2)
        time = []
        reader = open(logfile, 'r')
        line = reader.readline()
        timeTagTxt.write('\n' + '=' * 20 + ' Time Tag Start ' + '=' * 20 + '\n')
        while not line == '':
            if "bash arg:" in line:
                timeTagTxt.write(line)
            if "system_uptime:" in line:
                timeTagTxt.write(line)
                time.append(line.strip().split(' ')[3].split(':')[1].strip(']'))
            # print(line)
            if "CRASH:" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "NOT RESPONDING" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "No activities found to run, monkey aborted" in line:
                errorTxt.write(line)
                timeTagTxt.write(line)
            if "Monkey finished" in line:
                timeTagTxt.write(line)
            if "Network stats" in line:
                timeTagTxt.write(line)
            line = reader.readline()
        # calc monkey running time
        start = int(time[0])
        end = int(time[-1])
        print("start =" + str(start))
        print("end =" + str(end))
        runtime = timeShift(end - start)
        timeTagTxt.close()
        timeTagTxt = open(timeTagfile, 'r')
        lines = []
        for line in timeTagTxt:
            lines.append(line)
        timeTagTxt.close()
        print("lines = " + str(lines))

        res_str = '\n\n' + '=' * 20 + ' Test Result ' + '=' * 20 + '\n' + "StartTimeTag: %s\nEndTimeTag: %s\n" \
                  % (start, end) + "TotalRuntime: %d hor %d min %d sec\n" % (runtime[0], runtime[1], runtime[2]) + \
                  'Monkey Running time >6h :%s\n\n\n' % (runtime[0] > 6)
        lines.insert(0, res_str)
        str_res = ''.join(lines)
        timeTagTxt = open(timeTagfile,'w')
        timeTagTxt.write(str_res)
        timeTagTxt.close()
        errorTxt.close()
        haserror = get_error_time(errorfile)
        print("Analyse Result Finished...")
    else:
        print("Monkey log file isn`t exists.")
    return haserror


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
        str_error = re.sub(u"\\(.*?\\)", "", line.strip().strip("// ")).strip()
        print(str(str_error))
        if str_error in tmp.keys():
            tmp[str_error] = tmp[str_error] + 1
        else:
            tmp[str_error] = 1
        line = reader.readline()
    # print tmp
    for key in tmp.keys():
        errorCount.writelines(key + '=' + str(tmp[key]) + '\n')
    errorCount.close()

    if tmp:
        return True
    else:
        return False


def pullAllLog(sn, path):
    print('pulling %s logs...' % sn)
    local_time = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
    logpath = path + os.sep + 'Log_' + sn[-6:] + '_' + local_time + os.sep
    if not os.path.exists(logpath):
        os.system('mkdir %s' % (logpath))
    os.system('adb -s %s root' % sn)
    os.system('adb -s %s remount' % sn)
    print("logpath = " + logpath)
    os.system('mkdir %smtklog' % (logpath))
    os.system('adb -s %s pull /sdcard/mtklog %smtklog' % (sn, logpath))
    time.sleep(5)
    os.system('mkdir %sdata_aee_exp' % (logpath))
    os.system('adb -s %s pull /data/aee_exp %sdata_aee_exp' % (sn, logpath))
    os.system('mkdir %sdata_vendor_mtklog_aee_exp' % (logpath))
    os.system('adb -s %s pull /data/vendor/mtklog/aee_exp %sdata_vendor_mtklog_aee_exp' % (sn, logpath))
    os.system('mkdir %sdata_log' % (logpath))
    os.system('adb -s %s pull /data/log %sdata_log' % (sn, logpath))
    os.system('mkdir %sdropbox' % (logpath))
    os.system('adb -s %s pull /data/system/dropbox %sdropbox' % (sn, logpath))
    os.system('mkdir %sdata_tombstone' % (logpath))
    os.system('adb -s %s pull /data/tombstones %sdata_tombstone' % (sn, logpath))
    os.system('mkdir %slog' % (logpath))
    os.system('adb -s %s pull /log %slog' % (sn, logpath))
    os.system('mkdir %sdata_anr' % (logpath))
    os.system('adb -s %s pull /data/anr %sdata_anr' % (sn, logpath))
    os.system('mkdir %spstore' % (logpath))
    os.system('adb -s %s pull /sys/fs/pstore %spstore' % (sn, logpath))
    os.system('adb -s %s shell "getprop ro.versions.internal_sw_ver" >%sversion.txt' % (sn, logpath))


if __name__ == '__main__':
    for sn in get_sn():
        tag = get_phone_tag(sn)
        monkeylogPath = os.getcwd() + os.sep + tag
        if os.path.exists(monkeylogPath):
            pass
        else:
            os.mkdir(monkeylogPath)
        logPath = get_monkey_log(sn, monkeylogPath)
        print(logPath)
        hasError = analysisMonkeylog(logPath)
        if hasError:
            print("has error")
            pullAllLog(sn, monkeylogPath)
        else:
            print("No errors founded")
