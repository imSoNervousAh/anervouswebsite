# -*- coding: utf-8 -*-
from operator import itemgetter


def get_pending_applications():
    item1 = {'name': '计四五微信平台',
             'manager_name': '李三胖',
             'description': '计45班的班级微信公众号平台。'
             }
    item2 = {'name': '你说取这么长的名字会不会被打啊',
             'manager_name': '阿不思·珀西瓦尔·伍尔弗里克·布赖恩·邓布利多',
             'description': '你一定没见过这么标准的十五个字\n你一定没见过这么标准的十五个字\n你一定没见过这么标准的十五个字\n'
                            '你一定没见过这么标准的十五个字你一定没见过这么标准的十五个字你一定没见过这么标准的十五个字'
             }
    return [item1, item2]


def get_applications():
    item1 = {'name': '计四五微信平台',
             'description': '计45班的班级微信公众号平台。',
             'status': 'pending',
             'operator_admin_name': ''
             }
    item2 = {'name': '通过示范',
             'description': '一个申请通过的微信公众号平台。',
             'status': 'approved',
             'operator_admin_name': 'admin1'
             }
    item3 = {'name': '尚未提交示范',
             'description': '一个这边还没有提交上去的申请',
             'status': 'not_submitted',
             'operator_admin_name': ''
             }
    item4 = {'name': '拒绝示范',
             'description': '一个申请被拒的微信公众号平台。',
             'status': 'rejected',
             'operator_admin_name': 'admin3'
             }
    return [item1, item2, item3, item4]


def get_official_accounts():
    item1 = {'name': '中老年生活',
             'subscribers': 128984,
             'description': '让你的中老年生活充满精彩。'
             }
    item2 = {'name': '每日谣言',
             'subscribers': 7276,
             'description': '绝不说假话。'
             }
    return sorted([item1, item2], key=itemgetter('subscribers'), reverse=True)


def get_articles():
    item1 = {'title': '100个实用的生活小窍门！快转发给你的朋友！',
             'official_account_name': '中老年生活',
             'official_account_id': 1234,
             'description': '假装这里有一段看上去还比较长的文章概要。。。。。。。。。。。。。。。。。。。',
             'likes': 1234567,
             'views': 21378218
             }
    item2 = {'title': '太吃惊了！手机还可以这么用！',
             'official_account_name': '每日谣言',
             'official_account_id': 5678,
             'description': '你每天都在用手机，但你知道你的手机有什么隐藏功能吗？\n不看不知道！为了你的家人朋友，赶快转发到朋友圈！',
             'likes': 12734,
             'views': 973272
             }
    return sorted([item1, item2], key=lambda x: x['views'] + x['likes'] * 100, reverse=True)
