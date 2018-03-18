# -*- coding: utf-8 -*-
__author__ = 'CQ'

from settings import DATABASES
from .db_service import MysqlServer


class UserSqlOperation(object):
    """ 执行mysql语句 """
    @staticmethod
    def check_adm_login(admname):
        db = MysqlServer(DATABASES)
        sql = "select `name`,`password`,`caption` from user,user_group " \
              "where user_group_id=gid and name='%s'" % admname
        ret = db.run_sql(sql)
        db.close()
        return ret
