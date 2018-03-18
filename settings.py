# -*- coding: utf-8 -*-
__author__ = 'CQ'
import os

settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        # cookie不会以明文存储在客户端，而是用此字符串加密cookie，然后才存储在客户端
        "cookie_secret": "AQAAALudVkKt/AYA0bLPykwXoIBRVYTO",
        # 当用户没有登录时，tornado会自动跳转的登录URL请求用户登录
        "login_url": "/login"
}

template_variables = dict(
    title=u'Docker Mangerment Platform',
    name=u'Docker Mangerment Platform',
    username="root",
)

NODE_LIST = ['node_ip', 'port']

COOKIE_NAME = "user_id"

HOST_IP = "192.168.180.128"

PRIVATE_REGISTRY = "192.168.180.128:5000"

DATABASES = dict(
    DB='docker',
    USERNAME='docker',
    PASSWORD='123456',
    HOST=HOST_IP,
    PORT=3306,
    CHAR_SET="utf8",
)






