#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    @File: evaluate.py
    @Create: 2020/7/12 15:25
    @Version: V1.0-base
    @Author: afeng
    @Contact: afeng616@gmail.com
    @Description: 教师评估
"""
try:
    from .login import WYULogin
except:
    from login import WYULogin

import datetime


class Evaluate:
    def __init__(self, path_conf, level='A'):
        self.level = level
        self.headers = {
            "Host": "jxgl.wyu.edu.cn",
            "Proxy-Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "http://jxgl.wyu.edu.cn",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "http://jxgl.wyu.edu.cn/xswjxx!teaList.action",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        self.session = WYULogin(path_conf).login()

    def get_tealist(self):
        url_tealist = 'http://jxgl.wyu.edu.cn/xswjxx!getTeaDataList.action'
        post_items = ['pdm', 'xnxqdm', 'pjdxlxdm', 'pjlxdm', 'pjdxdm', 'pjdxmc', 'pjdxbh', 'kcptdm', 'wjdm', "jxhjmc"]
        teaching_link_q = {  # jxhjmc=
            "讲课": "1003573,1003577,1003576,1003578,1003580,1003582,1003575,1003581",
            "上机": "1003592,1003600,1003597,1003598,1003595,1003599,1003593,1003596",
            "实习": "1003608,1003609,1003603,1003605,1003607,1003611,1003606,1003610",
            "体育": "1003584,1003587,1003588,1003589,1003590,1003591,1003585,1003586",
            "实验": "1003592,1003600,1003597,1003598,1003595,1003599,1003593,1003596"
        }
        print('>=获取教师评价列表=<')
        tea_json = self.session.post(url=url_tealist, headers=self.headers, data={"xnxqdm": self.get_semester()}).json()
        print(f'共{tea_json["total"]}条评价数据')
        tealist = tea_json['rows']

        tea, teas = {}, []
        for tea in tealist:
            for post_item in post_items:
                tea[post_item] = (tea[post_item])
            tea['wtdms'] = tea.pop('jxhjmc')
            tea['wtdms'] = teaching_link_q[tea['wtdms']]
            teas.append(tea)
        return tea_json['total'], teas

    def evaluate(self):
        eval_state = {
            "A": [
                "123482,123502,123497,123507,123517,123527,123492,123522",
                "优秀,优秀,优秀,优秀,优秀,优秀,优秀,优秀",
                "9.50,9.50,14.25,14.25,11.88,11.88,11.88,11.88"
            ],
            "B": [
                "123483, 123503, 123498, 123508, 123518, 123528, 123493, 123523",
                "良好,良好,良好,良好,良好,良好,良好,良好",
                "8.50,8.50,12.75,12.75,10.63,10.63,10.63,10.63"
            ],
            "C": [
                "123579,123619,123604,123609,123594,123614,123584,123599",
                "中等,中等,中等,中等,中等,中等,中等,中等",
                "7.50,7.50,11.25,11.25,9.38,9.38,9.38,9.38"
            ]
        }
        score = {
            "A": 95.02,
            "B": 85.02,
            "C": 75.02
        }
        evaluation_level = {
            "xmdmvals": eval_state[self.level][0],
            "xmmcs": eval_state[self.level][1],
            "xzfzs": eval_state[self.level][2],
            "wtpf": score[self.level],
            "jy": ""
        }
        url_evaluate = 'http://jxgl.wyu.edu.cn/xswjxx!savePj.action'
        data = {}
        total, teas = self.get_tealist()
        print('>=开始教师评价=<')
        for i in range(total):
            data.update(teas[i])
            data.update(evaluation_level)
            print(f'<{i + 1}>评价等级{self.level}')
            response = self.session.post(url=url_evaluate, headers=self.headers, data=data).text
            print(f'<{i + 1}>评价完成' if response is '1' else '未知错误，导致操作中断！错误状态:' + response)
        print('>=教师评价完成=<')

    def get_semester(self):
        today = str(datetime.date.today())
        if today[5:] > '09-00':
            return f'{today[:4]}01'
        else:
            return f'{int(today[:4]) - 1}02'


if __name__ == '__main__':
    print("""
     _ _ _ _ _ _     _ _ _ _ _ _        _ _ _ _    _ _ _ _ _ _   
     \ _ _    _ _\   \    _ _ _ _\    /    _ _ \   \ _ _    _ _\ 
          \   \ test  \   \_ _ _ _    \   \ _ _ _       \   \    
           \   \ some- \    _ _ _ _\   \ _ _ _ _  \      \   \   
            \   \ thing \   \_ _ _ _     _ _ _ _\  |      \   \  
             \_ _\ here! \_ _ _ _ _ _\   \ _ _ _ _ /       \_ _\ 
    """)
