#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import os
import sys
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (BASE_DIR)

sys.path.append(BASE_DIR)

DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}

LOG_LEVEL = logging.INFO

LOG_TYPES = {
    "transaction":"transactions.log",
    "access":"access.log",
    'shopping': 'shopping.log',
    'access': 'access.log',
}

LOG_DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/logs" % BASE_DIR
}

TRANSACTION_TYPE = {
    'repay':{'action':'plus', 'interest':0},
    'withdraw':{'action':'minus', 'interest':0.05},
    'transfer':{'action':'minus', 'interest':0.05},
    'consume':{'action':'minus', 'interest':0},
}

ACCOUNT_FORMAT = {
    """
    用户数据库格式
    {"enroll_date": "2017-07-02", "password": "abc", "id": 10000, "credit": 15000,
     "status": 0, "balance": 10000.0, "expire_date": "2021-01-01", "pay_day": 22}
    """
}