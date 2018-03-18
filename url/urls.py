# -*- coding: utf-8 -*-
__author__ = 'CQ'
from handler.node import Main, NodeManage, ContList, ContHandele, NodeAdd, NodeModify, \
        ContStart, ContStop, ContRestart, ContDestroy, ContCreate, ImgList, ImgModify, ImgPull, ImgPush, ContRemotion
from handler.user import Welcome, Login, Logout

urls = [
        (r'/', Welcome),
        (r'/login', Login),
        (r'/test', Welcome),
        (r'/logout', Logout),
        (r'/main', Main),
        (r'/nodemanage', NodeManage),
        (r'/nodeadd', NodeAdd),
        (r'/nodemodify', NodeModify),
        (r'/contlist', ContList),
        (r'/conthandle', ContHandele),
        (r"/constart", ContStart),
        (r"/constop", ContStop),
        (r"/conrestart", ContRestart),
        (r"/condestroy", ContDestroy),
        (r"/concreate", ContCreate),
        (r"/imglist", ImgList),
        (r"/imgmodify", ImgModify),
        (r"/imgpull", ImgPull),
        (r"/imgpush", ImgPush),
        (r"/imgpush", ImgPush),
        (r"/conremotion", ContRemotion),
    ]
