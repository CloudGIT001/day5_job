#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import json
import time
from core import db_handler
from conf import settings


def load_current_balance(account_id):
    """

    :param account_id:
    :return:
    """
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_id)
    with open(account_file) as f:
        acc_data = json.load(f)
        return acc_data

def load_account_info(account_id):
    """

    :param account_id:
    :return:
    """
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_id)
    with open(account_file) as f:
        acc_data = json.load(f)
        return acc_data


def dump_account(account_data):
    """

    :param account_data:
    :return:
    """
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_data['id'])
    with open(account_file, 'w') as f:
        acc_data = json.dump(account_data, f)
    return True

def dump_shop_account(account_data):
    """

    :param account_data:
    :return:
    """
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account_data['user'])
    with open(account_file, 'w') as f:
        acc_data = json.dump(account_data, f)
    return True