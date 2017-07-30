#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


import json
acc_dic = {
    'id': '1234',
    'password': 'abc123',
    'credit': 20000,
    'balance': 20000,
    'enroll_date': '2017-07-28',
    'expire_date': '2020-01-01',
    'pay_day': 22,
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled, 8 = admin

}

print(json.dumps(acc_dic))