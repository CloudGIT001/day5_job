#### ATM：模拟实现一个ATM + 购物商城程序

功能需求：
```
额度 15000或自定义
实现购物商城，买东西加入 购物车，调用信用卡接口结账
可以提现，手续费5%
支持多账户登录
支持账户间转账
记录每月日常消费流水
提供还款接口
ATM记录操作日志
提供管理接口，包括添加账户、用户额度，冻结账户等。。。
用户认证用装饰器
```

##### 程序结构
```
 ATM_作业练习
    │  ATM+购物商城程序.md
    │
    ├─bin
    │      atm.py
    │      manage.py
    │      shop.py
    │      __init__.py
    │
    ├─conf
    │  │  commodity.py
    │  │  settings.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          commodity.cpython-36.pyc
    │          settings.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │
    ├─core
    │  │  accounts.py
    │  │  auth.py
    │  │  bill_date.py
    │  │  db_handler.py
    │  │  logger.py
    │  │  main.py
    │  │  shopping.py
    │  │  transaction.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          accounts.cpython-36.pyc
    │          auth.cpython-36.pyc
    │          bill_date.cpython-36.pyc
    │          db_handler.cpython-36.pyc
    │          logger.cpython-36.pyc
    │          main.cpython-36.pyc
    │          shopping.cpython-36.pyc
    │          transaction.cpython-36.pyc
    │          __init__.cpython-36.pyc
    │
    ├─db
    │  │  account_sample.py
    │  │  __init__.py
    │  │
    │  └─accounts
    │          10001.json
    │          1010101.json
    │          abc123.json
    │          admin.json
    │          qwert.json
    │          test.json
    │          xiess.json
    │
    └─log
        │  access.log
        │  qwert_shopping.log
        │  shopping.log
        │  test_shopping.log
        │  transactions.log
        │  __init__.py
        │
        └─accounts
                abc123.bills
```

##### ATM信用卡中心功能介绍
ATM信用卡中心函数功能
```
1.  信用卡账户信息:
	account_info()
2.  信用卡还款:
	repay()
3.  信用卡取款:
	withdraw()
4.  信用卡转账:
	transfer()
0.  退出信用卡中心
	logout()
```

测试的帐号密码
```
帐号1： {"enroll_date": "2017-07-30", "balance": 20000, "password": "abc123", "id": "xiess", "credit": 20000, "status": 0, "expire_date": "2027-07-29", "pay_day": 22}

帐号2：{"enroll_date": "2017-07-28", "password": "abc123", "pay_day": 25, "credit": 20000, "id": "abc123", "balance": 19995.0, "status": 0, "expire_date": "2027-07-28"}
```

使用说明
```
运行环境：python3.6

依赖软件包：
import datetime
import time
import os
import json
import logging

脚本运行：
python atm.py
```

运行示例
```
-*-*-*-*-*-*-*--*-*- ATM信用卡中心 -*-*-*-*-*-*-*-*-*-*-*-

Account:abc123
Password:abc123

    -*-*-*-*-*-*- ATM信用卡中心 -*-*-*-*-*-*-
    1.  信用卡账户信息
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    0.  退出信用卡中心
    
>>>[0=exit]:1
enroll_date         :2017-07-28          
pay_day             :25                  
credit              :20000               
id                  :abc123              
balance             :19995.0             
status              :0                   
expire_date         :2027-07-28          

    -*-*-*-*-*-*- ATM信用卡中心 -*-*-*-*-*-*-
    1.  信用卡账户信息
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    0.  退出信用卡中心
    
>>>[0=exit]:2
-*-*-*-*-*-*-*-*- 账户余额信息 -*-*-*-*-*-*-*-*-
        Credit :    20000
        Balance:    19995.0
 请输入还款余额[q=quit]>>>:2000
2017-07-31 01:41:34,982 - transaction - INFO - account:abc123   action:repay    amount:2000.0   interest:0.0
还款后账目信息:21995.0
 请输入还款余额[q=quit]>>>:q

    -*-*-*-*-*-*- ATM信用卡中心 -*-*-*-*-*-*-
    1.  信用卡账户信息
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    0.  退出信用卡中心
    
>>>[0=exit]:3
 -*-*-*-*-*-*-*-*- 账户余额信息 -*-*-*-*-*-*-*-*-
        Credit :    20000
        Balance:    21995.0
请输入取款余额[q=quit]>>>:100
2017-07-31 01:41:57,683 - transaction - INFO - account:abc123   action:withdraw    amount:100.0   interest:5.0
余额总数:21890.0
请输入取款余额[q=quit]>>>:q

    -*-*-*-*-*-*- ATM信用卡中心 -*-*-*-*-*-*-
    1.  信用卡账户信息
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    0.  退出信用卡中心
    
>>>[0=exit]:4
 -*-*-*-*-*-*-*-*- 账户信息 -*-*-*-*-*-*-*-*-
        Credit :    20000
        Balance:    21890.0
        
收款人:[q=quit]>>>:xiess
收款金额:[q=quit]100
2017-07-31 01:42:17,476 - transaction - INFO - account:abc123   action:transfer    amount:100.0   interest:5.0
Transaction type [receive] is not exist!
帐号余额:21785.0
收款人:[q=quit]>>>:q

    -*-*-*-*-*-*- ATM信用卡中心 -*-*-*-*-*-*-
    1.  信用卡账户信息
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    0.  退出信用卡中心
    
>>>[0=exit]:0
-*-*-*-*-*-*-*-*- 再见 -*-*-*-*-*-*-*-*-
```


##### 管理员平台中心功能介绍

函数功能介绍
```
退出管理平台: 'logout(acc_data)',
创建用户信息: 'auth.sign_up()',
查询用户信息: 'account_info(acc_data)',
修改用户信息: 'auth.modify()',
生成用户帐单: 'get_all_bill()',
```


测试帐号信息
```
帐号1：{"enroll_date": "2017-07-18", "password": "abc123", "id": "admin", "credit": 10000, "status": 8, "balance": 10000.0, "expire_date": "2020-01-01", "pay_day": 0}
```



使用说明
```
运行环境：python3.6

依赖软件包：
import datetime
import time
import os
import json
import logging

脚本运行：
python manage.py
```

使用示例：
```
-*-*-*-*-*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-*-*-*-*-

Account:admin
Password:abc123

    -*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-
    0.  退出管理平台
    1.  创建用户信息
    2.  查询用户信息
    3.  修改用户信息
    4.  生成用户帐单
    5.  修改用户信用卡信息
请输入操作[0=exit]>>>:1
account id:10001
password:100001
用户添加成功

    -*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-
    0.  退出管理平台
    1.  创建用户信息
    2.  查询用户信息
    3.  修改用户信息
    4.  生成用户帐单
    5.  修改用户信用卡信息
请输入操作[0=exit]>>>:2
请输入查找用户的ID:>>>:xiess
enroll_date         :2017-07-18          
id                  :admin               
credit              :10000               
status              :8                   
balance             :10000.0             
expire_date         :2020-01-01          
pay_day             :0                   

    -*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-
    0.  退出管理平台
    1.  创建用户信息
    2.  查询用户信息
    3.  修改用户信息
    4.  生成用户帐单
    5.  修改用户信用卡信息
请输入操作[0=exit]>>>:3
account id:xiess
josn格式:{"credit":30000,"pay_day": 23}
请输入修改内容[json格式]>>>:{"credit":20000,"pay_day": 23}
{"credit":20000,"pay_day": 23}
用户数据更新成功！

    -*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-
    0.  退出管理平台
    1.  创建用户信息
    2.  查询用户信息
    3.  修改用户信息
    4.  生成用户帐单
    5.  修改用户信用卡信息
请输入操作[0=exit]>>>:4
生成帐单
生成帐单

    -*-*-*-*-*-*- 管理员平台 -*-*-*-*-*-*-
    0.  退出管理平台
    1.  创建用户信息
    2.  查询用户信息
    3.  修改用户信息
    4.  生成用户帐单
    5.  修改用户信用卡信息
请输入操作[0=exit]>>>:0
-*-*-*-*-*-*-*-*- 再见 -*-*-*-*-*-*-*-*-
```

##### 购物商城

函数功能介绍
```
退出 logout()
注册用户帐号 sign_up(user_data)
登录商城 logout()
购物车函数 show_shopping_cart(user_data, all_cost)
购物函数 go_shopping(log_obj,account_data)
充值转账函数 charge_money(money)  ---> 功能未实现
```

测试帐号信息
```
帐号1：{"enroll_date": "2017-07-30", "balance": 16890, "password": "abc1234", "user": "qwert", "status": 0}
帐号2：{"status": 0, "enroll_date": "2017-07-28", "user": "test", "password": "test", "balance": 400000}
```

使用说明
```
运行环境：python3.6

依赖软件包：
import datetime
import time
import os
import json
import logging

脚本运行：
python stop.py
```

使用示例：
```
-*-*-*-*-*-*-*--*-*- 购物商城 -*-*-*-*-*-*-*-*-*-*-*-


    0.  退出
    1.  登录商城
    2.  注册帐号
    
[0=exit]>>>:1
用户名ID>>>:qwert
用户密码>>>:abc123
Account or password is incorrect!
用户名ID>>>:qwert
用户密码>>>:abc1234
----------------------商品列表信息----------------------
0 --> ('iphone7', 5188)
1 --> ('xiaomi5', 1888)
2 --> ('huaweip9', 2899)
3 --> ('python_book', 49)
4 --> ('java_book', 60)
5 --> ('linux_book', 75)
6 --> ('management_book', 30)
7 --> ('Milk', 59)
8 --> ('Coffee', 30)
9 --> ('Tea', 311)
提示：q=退出]；t=[充值账户];c=[打印购物车]
请选择产品标号:3
10
请输入购买数量:10
Added [2017-07-31 02:35:16,201 - shopping - INFO - account:qwert action:shopping product_number:10 goods:python_book cost:490
10] [python_book] into shopping cart,your balance is [19510]
----------------------商品列表信息----------------------
0 --> ('iphone7', 5188)
1 --> ('xiaomi5', 1888)
2 --> ('huaweip9', 2899)
3 --> ('python_book', 49)
4 --> ('java_book', 60)
5 --> ('linux_book', 75)
6 --> ('management_book', 30)
7 --> ('Milk', 59)
8 --> ('Coffee', 30)
9 --> ('Tea', 311)
提示：q=退出]；t=[充值账户];c=[打印购物车]
请选择产品标号:q
------------------------再见------------------------
**********************购物车列表***********************
Goods                Price           Number     Cost                
python_book          49              10         490                 
***********************End************************
You total cost:                                 490                 
Your balance is [19510]

-*-*-*-*-*-*-*--*-*- 购物商城 -*-*-*-*-*-*-*-*-*-*-*-


    0.  退出
    1.  登录商城
    2.  注册帐号
    
[0=exit]>>>:2
注册用户ID:1010101
用户密码:1010101
用户信息注册完成

    0.  退出
    1.  登录商城
    2.  注册帐号
    
[0=exit]>>>:0

----------- 退出成功 -----------
```



#### ATM+购物商城程序缺陷
1、 对用户使用的日志信息打印不明显
2、 ATM信用卡与购物商城的扣款API接口未实现
3、 帐号的功能只能单一使用。三个平台的用户不能都同时访问
4、 管理员在生产用户账单时，会抛出异常
......




