#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import logging
import datetime
from conf import settings
from core import bill_date


def logger(log_type,*args):
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)

    log_file = "%s/log/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def show_log(account,log_type,year_mount):
    begin_time,end_time = bill_date.get_time(year_mount)
    log_file = "%s/log/%s"%(settings.BASE_DIR,settings.LOG_TYPES[log_type])
    file = open(log_type)

    for line in file:
        log_time = datetime.datetime.strptime(line.split(",")[0],"%Y-%m-%d %H:%M:%S")
        user_name = line.split()[7].split(":")[1]
        if account == user_name and begin_time <= log_time < end_time:
            print (line.strip())
        file.close()


def show_shop_log(user_name, log_type):
    """
    显示消费日志内容
    :param user_name: 用户名
    :param log_type: 日志类型
    :return:
    """
    log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name, settings.LOG_TYPES[log_type])
    file = open(log_file)
    print("-".center(50, "-"))

    for line in file:
        print(line.strip())
    file.close()