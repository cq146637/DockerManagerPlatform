# -*- coding: utf-8 -*-
__author__ = 'CQ'

import pymysql
import logging


logger = logging.getLogger(__name__)


class MysqlServer(object):
    """
        Tornado通用连接数据库类
        用pymysql替代tornado使得操作数据库更加灵活，定制化
    """

    def __init__(self, db_config):
        try:
            self._db_config = db_config
            self._conn = self.__get_conn()
            self._cursor = self._conn.curson()
        except Exception:
            self.close()
            logger.exception(u"数据库连接失败")

    def __get_conn(self):
        connection = pymysql.connect(host=self._db_config['HOST'],
                                     port=self._db_config['PORT'],
                                     user=self._db_config['USERNAME'],
                                     password=self._db_config['PASSWORD'],
                                     db=self._db_config['DB_NAME'],
                                     charset=self._db_config['CHAR_SET'],
                                     )
        connection.ping(True)
        return connection

    def ensure_cursor(self):
        if not self._cursor:
            if not self._conn:
                self._conn = self.__get_conn()
            self._cursor = self._conn.cursor()

    def run_sql(self, sql):
        """
            执行完SQL语句需要返回结果
        :param sql:
        :return:
        """
        self.ensure_cursor()
        self._cursor.execute(sql)
        # commit只对innodb生效，不加commit的话，修改数据库记录的操作不会生效。
        # 如果是myisam引擎的话，不需要commit即可生效
        self._conn.commit()
        return self._cursor.fetchall()

    def execute_sql(self, sql):
        """
            执行SQL语句无返回值
        :param sql:
        :return:
        """
        self.ensure_cursor()
        self._cursor.execute(sql)
        self._conn.commit()

    def run_sql_fetchone(self, sql):
        """
            执行SQL返回一条结果
        :param sql:
        :return:
        """
        self.ensure_cursor()
        self._cursor.execute(sql)
        return self._cursor.fetchone()

    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
        logger.info(u"关闭数据库连接")


def test():
    settings = {
        'HOST': "127.0.0.1",
        'PORT': "3306",
        'USERNAME': "root",
        'PASSWORD': "123456",
        'DB_NAME': "test",
        'CHAR_SET': "utf8",
    }
    db = MysqlServer(settings)
    sql = "select distinct `node_name` from tb_node"
    ret = db.run_sql(sql)
    db.close()
    return ret


if __name__ == "__main__":
    print(test())
