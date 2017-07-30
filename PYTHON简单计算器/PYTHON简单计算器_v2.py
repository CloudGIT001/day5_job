#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:xieshengsen


"""
模拟计算器开发：
实现加减乘除及拓号优先级解析
用户输入 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )等类似公式后，
必须自己解析里面的(),+,-,*,/符号和公式(不能调用eval等类似功能偷懒实现)，运算后得出结果，结果必须与真实的计算器所得出的结果一致
"""


import re
import sys

def multiply_divide(args):
    """
    乘除法函数，匹配表达式中的乘除法表达式，并且将乘除法表达式返回
    :param args:
    :return:
    """
    values = args[0]
    pattern = re.compile(r"\d+\.?\d*[\*\/\%\/\/]+[\+\-]?\d+\.*\d*")    #匹配表达式的乘除法运算

    match = pattern.search(values)
    if not match:
        return

    connect = pattern.search(values).group()
    if len(connect.split("*")) > 1:
        n1, n2 = connect.split("*")
        value = float(n1) * float(n2)

    if len(connect.split("//")) > 1:
        n1, n2 = connect.split("//")
        value = float(n1) // float(n2)

    if len(connect.split("%")) > 1:
        n1, n2 = connect.split('%')
        value = float(n1) % float(n2)

    if len(connect.split("/")) > 1:
        n1, n2 = connect.split("/")
        value = float(n1) / float(n2)

    before,after = pattern.split(values,1)
    new_result = "%s%s%s"%(before,value,after)
    args[0] = new_result
    return multiply_divide(args)


def addition_subtraction(args):
    """
    加减法函数，匹配表达式中的加减法表达式，将加减法表达式返回
    :param args:
    :return:
    """
    # while True:
    args[0] = args[0].replace('+-', '-')
    args[0] = args[0].replace('++', '+')
    args[0] = args[0].replace('-+', '-')
    args[0] = args[0].replace('--', '+')

    if args[0].startswith("-"):
            args[1] += 1
            args[0] = args[0].replace("-","&")
            args[0] = args[0].replace("+","-")
            args[0] = args[0].replace("&", "+")
            args[0] = args[0][1:]

    values = args[0]
    pattern = re.compile(r"\d+\.?\d*[\+\-]{1}\d+\.?\d*")   # 匹配表达式的加减法

    match = pattern.search(values)
    if not match:
        return

    connect = pattern.search(values).group()
    if len(connect.split("+")) > 1:
        n1, n2 = connect.split("+")
        value = float(n1) + float(n2)

    else:
        n1, n2 = connect.split('-')
        value = float(n1) - float(n2)

    before, after = pattern.split(values, 1)
    new_result = "%s%s%s"%(before,value,after)
    args[0] = new_result
    return addition_subtraction(args)


def operation(expression):
    """
    运算函数，获取到乘除法和加减法的表达式，并且将运算结果返回
    :param expression:
    :return:
    """
    express = [expression,0]
    print (express)

    multiply_divide(express)
    addition_subtraction(express)

    if divmod(express[1],2)[1] == 1:
        result = float(express[0])
        result = result * -1

    else:
        result = float(eval(express[0]))

    print("\033[31;1mresult>>:\033[0m",result)
    return result


def operation_brackets(expression):
    """
    括号匹配函数，匹配表达式中带有括号的表达式
    :param expression:
    :return:
    """
    pattern = re.compile(r"\(([\+\-\*\/\%\/\/\*\*]*\d+\.*\d*){2,}\)")    # 匹配只有一层括号的表达式
    if not pattern.search(expression):
        final = operation(expression)
        return final

    content = pattern.search(expression).group()
    first_result, second_result, oper_result = pattern.split(expression, 1)
    # print("oper_result:", expression)
    content = content[1:len(content) - 1]

    ret = operation(content)
    # print ("%s=%s"%(content,ret))

    expression = "%s%s%s" %(first_result, ret, oper_result)
    print('\033[31;1moper_result\033[0m:', expression)
    return operation_brackets(expression)


def main():
    """
    计算器主函数，用于用户输入运算表达式。并且判断表达式是否合法
    :return:
    """
    exit_flag = True
    while exit_flag:

        user_input = input("请输入运算表达式[q=quit]>>>:")
        user_input = re.sub("\s*","",user_input)  # 匹配输入的内容是否有空

        if len(user_input) == 0:
            continue

        if user_input == "q":
            print ("\033[42;1m成功退出计算器\033[0m")
            sys.exit()
            # exit_flag = False

        if re.search("[^0-9\.\-\+\*\/\%\/\/\*\*\(\)]",user_input):  # 匹配表达式是否含有字母
            print ("\033[41;1m输入有误，请重新输入\033[0m")

        else:
            result = operation_brackets(user_input)
            print (result)


if __name__ == "__main__":
    print ("*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*\n"
           "*                                                  *\n"
           "*              欢迎使用PYTHON简易计算器               *\n"
           "*                                                  *\n"
           "*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*\n")

    input("\033[31;1m输入表达式不能带空格或带英文字符\033[0m按任意键继续:")

    main()