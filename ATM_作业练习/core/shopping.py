#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen

from core import auth
from core import logger
from core import accounts
from conf import settings
from conf import commodity
from core import db_handler
import time
import json
import datetime
import os
import subprocess

access_logger = logger.logger('access')
shopping_cart = {}
all_cost = 0

user_data = {
    'is_authenticated': False,
    'account_data': None
}


def interactive():
    menu = '''
    0.  退出
    1.  登录商城
    2.  注册帐号
    '''
    menu_dic = {
        '1': 'login()',
        '2': 'sign_up(user_data)',
        '0': 'logout()'
    }
    exit_flag = False
    while not exit_flag:
        print(menu)
        user_option = input("[0=exit]>>>:").strip()
        if user_option in menu_dic.keys():
            exit_flag = eval(menu_dic[user_option])
        else:
            print("\033[31;1m操作错误\033[0m")


def login():
    acc_data = acc_login(user_data, access_logger)
    if user_data['is_authenticated']:
        user_data['account_data'] = acc_data
        return True


def logout():

    exit("\n----------- 退出成功 -----------")


def show_shopping_cart(user_data, all_cost):
    if user_data['is_authenticated'] is True:
        account_data = user_data['account_data']  # 用户信息
        money = account_data['balance']  # 当前帐户余额

        print("购物车列表".center(50, "*"))
        print("%-20s %-15s %-10s %-20s" % ("Goods", "Price", "Number", "Cost"))
        for key in shopping_cart:
            p_name = key[0]
            p_price = int(key[1])
            p_number = int(shopping_cart[key])
            print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % (p_name, p_price, p_number, p_price * p_number))
        print("End".center(50, "*"))
        print("%-20s %-15s %-10s \033[32;1m%-20s\033[0m" % ("You total cost:", "", "", all_cost))
        print("Your balance is [\033[32;1m%s\033[0m]" % money)
        accounts.dump_shop_account(account_data)


def sign_up(user_data):
    exist_flag = True
    while exist_flag is True:
        user = input("\033[32;1m注册用户ID:\033[0m").strip()
        password = input("\033[32;1m用户密码:\033[0m").strip()
        exist_flag = acc_check(user)
        if exist_flag:
            print("%s用户ID已经存在，请注册其他用户ID" % user)
            exist_flag = True
            continue
        else:
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            account_data = {"enroll_date": today, "balance": 0, "password": password, "user": user, "status": 0}
            accounts.dump_shop_account(account_data)
            user_data['is_authenticated'] = True
            user_data['user'] = user
            user_data['account_data'] = account_data
            print ("用户信息注册完成")
            return interactive()


def acc_auth(account, password):
    global new_user
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)

    if os.path.isfile(account_file):
        new_user = False

        with open(account_file, 'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                return account_data
            else:
                print("\033[31;1mAccount or password is incorrect!\033[0m")
    else:
        new_user = True
        print("Account [\033[31;1m%s\033[0m] does not exist!" % account)


def acc_login(user_data,log_obj):
    retry_count = 0
    same_user_count = 0
    last_user = ""

    while user_data['is_authenticated'] is not True and retry_count < 3:
        user = input("\033[32;1m用户名ID>>>:\033[0m").strip()
        password = input("\033[32;1m用户密码>>>:\033[0m").strip()
        if last_user == user:
            same_user_count += 1
        auth = acc_auth(user, password)
        if auth:
            user_data['is_authenticated'] = True
            user_data['user'] = user
            money = auth["balance"]
            old_money = money
            return auth
        last_user = user
        retry_count += 1

    else:
        print(same_user_count)
        if same_user_count == retry_count - 1:
            log_obj.error("account [%s] too many login attempts" % user)


def acc_check(account):
    db_path = db_handler.db_handler(settings.DATABASE)
    account_file = "%s/%s.json" % (db_path, account)
    if os.path.isfile(account_file):
        with open(account_file, 'r') as f:
            account_data = json.load(f)
            return account_data


def show_shopping_history(user_name, log_type):
    log_file = "%s/log/%s_%s" % (settings.BASE_DIR, user_name, settings.LOG_TYPES[log_type])
    if os.path.getsize(log_file):
        see_history = input("Please input:").strip()
        if see_history == "y" or see_history == "yes":
            logger.show_log(user_name, log_type)


def list_one_layer():

    one_layer_list = []
    print("商品列表信息".center(50, "-"))
    for index, item in enumerate(commodity.menu):
        print("\033[32;1m%d\033[0m --> %s" % (index, item))
        one_layer_list.append(item)

    print("\n提示：q=退出]；t=[充值账户];c=[打印购物车]")
    once_choice = input("请选择操作内容[q=quit]>>>:").strip()
    if once_choice.isdigit():
        once_choice = int(once_choice)
        if 0 <= once_choice < len(commodity.menu):
            print("---->Enter \033[32;1m%s\033[0m" % (one_layer_list[once_choice]))
            two_layer_list = commodity.menu[one_layer_list[once_choice]]
            return two_layer_list
        else:
            print("\033[31;1m输入错误，请重新输入\033[0m")
    else:
        if once_choice == "q":
            show_shopping_cart(user_data, all_cost)
            time.sleep(0.1)
            exit("再见".center(25, "-"))

        elif once_choice == "c":
            show_shopping_cart(user_data, all_cost)

        elif once_choice == "t":
            account_data = user_data['account_data']
            money = account_data['balance']
            money = charge_money(money)
            user_data['account_data']['balance'] = money

        else:
            print("\033[31;1m请输入数字\033[0m")
    return None


def charge_money(money):
    exit_flag = False
    while exit_flag is not True:
        user_charge = input("是否提取信用卡余额[\033[32;1my|n|b]\033[0m").strip()
        if user_charge == "y":
            print("信用卡支付")
            while True:
                charge_number = input("请输入您的充值金额:").strip()
                if charge_number.isdigit():
                    pass
        return money


def go_shopping(log_obj,account_data):

    global all_cost
    flag = False
    exit_flag = False
    while not exit_flag:

        print("商品列表信息".center(50, "-"))

        for index, item in enumerate(commodity.menu):
            print("\033[32;1m%d\033[0m --> %s" % (index, item))

        print("\033[32;1m提示：q=退出]；t=[充值账户];c=[打印购物车]\033[0m")
        user_choice = input("请选择产品标号:").strip()
        if user_choice.isdigit():
            user_choice = int(user_choice)
            print (len(commodity.menu))

            if 0 <= user_choice < len(commodity.menu):
                product_number = input("请输入购买数量:").strip()
                if product_number.isdigit():
                    product_number = int(product_number)
                else:
                    continue

            p_item = commodity.menu[user_choice]
            p_name = p_item[0]
            p_price = int(p_item[1])
            new_added = {}
            money = 20000
            if p_price * product_number <= money:
                new_added = {p_item: product_number}
                for k, v in new_added.items():
                    if k in shopping_cart.keys():
                        shopping_cart[k] += v
                    else:
                        shopping_cart[k] = v
                money -= p_price * product_number
                all_cost += p_price * product_number
                log_obj.info("account:%s action:%s product_number:%s goods:%s cost:%s" %
                             (account_data['user'], "shopping", product_number, p_name, all_cost))
                print("Added [\033[32;1m%d\033[0m] [\033[32;1m%s\033[0m] into shopping cart,"
                      "your balance is [\033[32;1m%s\033[0m]" % (product_number, p_name, money))
                time.sleep(0.1)

            else:
                print("Your balance is [\033[31;1m%s\033[0m],cannot afford this.." % money)
            user_data['account_data']['balance'] = money

        else:
            if user_choice == "q":
                show_shopping_cart(user_data, all_cost)
                exit("再见".center(50, "-"))
            elif user_choice == "c":
                show_shopping_cart(user_data, all_cost)
            elif user_choice == "b":
                exit_flag = True
            else:
                print("输入错误")


def shop_run():
    print("\n-*-*-*-*-*-*-*--*-*- 购物商城 -*-*-*-*-*-*-*-*-*-*-*-\n")
    interactive()

    account_data = user_data['account_data']
    user_name = account_data['user']

    log_type = "shopping"
    shopping_logger = logger.logger(log_type, user_name)
    show_shopping_history(user_name, log_type)
    go_shopping(shopping_logger, user_data)


