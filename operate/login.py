#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    @File: login.py
    @Create: 2020/7/12 12:23
    @Version: V1.0-base
    @Author: afeng
    @Contact: afeng616@gmail.com
    @Description: wyu登录
"""

import os
import requests
import configparser

try:
    from model.WYU_ResNet_captcah import UseCPU
except:
    from .model.WYU_ResNet_captcah import UseCPU

from io import BytesIO
from PIL import Image


class WYULogin:
    def __init__(self, path_conf):
        # 配置文件读取账号、密码
        self.cf = configparser.ConfigParser()
        self.path_conf = os.path.join(path_conf, 'account.ini')
        self.cf.read(self.path_conf, 'utf-8')
        print('>=自account.ini读取WYU学号、密码=<')
        if not os.path.exists(self.path_conf):
            print(f'未在指定目录({self.path_conf})找到account.ini文件')
        print('若account.ini文件中无登录数据请在命令行中手动输入')
        self.session = requests.session()
        account = self.cf.get('WYU', 'account')
        self.account = account if account is not '' else input('请输入WYU学号:')
        pwd = self.cf.get('WYU', 'pwd')
        self.pwd = pwd if pwd is not '' else input('请输入WYU密码:')
        print(f'获取WYU学号:{self.account}/密码:{self.pwd}')
        self.account_update()

    def login(self):
        url_login = 'http://jxgl.wyu.edu.cn/new/login'
        yzm = self.yzm_process()
        data = {
            'account': self.account,
            'pwd': self.pwd,
            'verifycode': yzm
        }
        print('>=WYU尝试登录=<')
        text = self.session.post(url_login, data=data).text
        while '登录成功' not in text:
            if '验证码不正确' in text:
                print('验证码自动识别错误，尝试再次识别')
                yzm = self.yzm_process()
                data.update({'verifycode', yzm})
            else:
                print(f'WYU账号、密码不正确({self.account}|{self.pwd})')
                self.account = input('请重新输入WYU学号:')
                self.pwd = input('请重新输入WYU密码:')
                self.account_update()
                yzm = self.yzm_process()
                data.update({'verifycode', yzm})
            print('>=WYU尝试登录=<')
            text = self.session.post(url_login, data=data).text
        print('>=WYU登录成功=<')
        return self.session

    def yzm_process(self):
        url_yzm = 'http://jxgl.wyu.edu.cn/yzm'
        print('>=验证码识别=<')
        print('>=获取WYU系统验证码=<')
        yzm_response = self.session.get(url_yzm)  # 获取验证码响应
        yzm_img = Image.open(BytesIO(yzm_response.content))
        print('>=验证码识别=<')
        t, yzm = UseCPU(yzm_img)  # 识别时间、识别结果
        print(f'验证码识别花费时间:{t}s')
        return yzm

    def account_update(self):
        print('>=account.ini数据更新=<')
        self.cf.set('WYU', 'account', self.account)
        self.cf.set('WYU', 'pwd', self.pwd)
        self.cf.write(open(self.path_conf, 'r+', encoding='utf-8'))


if __name__ == '__main__':
    print("""
     _ _ _ _ _ _     _ _ _ _ _ _        _ _ _ _    _ _ _ _ _ _   
     \ _ _    _ _\   \    _ _ _ _\    /    _ _ \   \ _ _    _ _\ 
          \   \ test  \   \_ _ _ _    \   \ _ _ _       \   \    
           \   \ some- \    _ _ _ _\   \ _ _ _ _  \      \   \   
            \   \ thing \   \_ _ _ _     _ _ _ _\  |      \   \  
             \_ _\ here! \_ _ _ _ _ _\   \ _ _ _ _ /       \_ _\ 
    """)
    WYULogin('../').login()
