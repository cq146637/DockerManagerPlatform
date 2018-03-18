# -*- coding: utf-8 -*-
__author__ = 'CQ'
from settings import DATABASES
from .db_service import MysqlServer


class NodeInfo(object):
    @staticmethod
    def user_access(username):
        db = MysqlServer(DATABASES)
        sql = "select node_group.gid, user_group.gid from node_group,user_group,user where " \
              "user.user_group_id=user_group.gid and user_group.gid=node_group.gid and user.name='%s';" % username
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def node_info():
        db = MysqlServer(DATABASES)
        sql = "select node.*,node_group.caption,user_group.caption rule from node,node_group,user_group where " \
              "node.node_group_id=node_group.gid and user_group.gid=node.node_group_id"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def group_list():
        db = MysqlServer(DATABASES)
        sql = "select distinct `node_group_id` from node"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def node_list(node_group_id,user_group_id):
        db = MysqlServer(DATABASES)
        sql = "select `ip`, `port` from node where node_group_id='%s' and user_group_id='%s'" %\
              (node_group_id, user_group_id)
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_node_port(node_ip):
        db = MysqlServer(DATABASES)
        sql = "select `port` from node where ip='%s'" % node_ip
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def insert_con_usage(con_id, con_ip, node_ip):
        db = MysqlServer(DATABASES)
        sql = "insert into con_usage(con_id, con_ip, node_ip) values('%s','%s','%s')" % (con_id, con_ip, node_ip)
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def delete_con_usage(con_id):
        db = MysqlServer(DATABASES)
        sql = "delete from con_usage where con_id='%s'" % con_id
        db.execute_sql(sql)
        db.close()
        return 0

    @staticmethod
    def con_usage_info():
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`node_ip`,`user_name`,`con_app`,`con_desc` from con_usage;"
        result = db.run_sql(sql)
        db.close()
        return result

    @staticmethod
    def get_con_usage_modify(result):
        db = MysqlServer(DATABASES)
        sql = "select `con_id`,`con_ip`,`node_ip`,`user_name`,`con_app`,`con_desc` " \
              "from con_usage where con_id='%s'" % result
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_all_node():
        db = MysqlServer(DATABASES)
        sql = "select `ip` from node;"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def get_group_list():
        db = MysqlServer(DATABASES)
        sql = "select node_group.gid, node_group.caption, user_group.gid, user_group.caption from " \
              "node_group,user_group;"
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def save_node(node_dict):
        db = MysqlServer(DATABASES)
        sql = "insert into node (name,ip,port,cpus,mem,images,state,containers,os_version," \
              "kernel_version,docker_version,node_group_id,user_group_id) " \
              "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                node_dict["node_name"],
                node_dict["node_ip"],
                node_dict["node_port"],
                node_dict["node_cpus"],
                node_dict["node_mem"],
                node_dict["node_imgs"],
                node_dict["node_state"],
                node_dict["node_cons"],
                node_dict["node_os"],
                node_dict["node_ks"],
                node_dict["node_ds"],
                node_dict["node_group"],
                node_dict["user_group"],)
        ret = db.run_sql(sql)
        db.close()
        return ret

    @staticmethod
    def delete_node(node_ip):
        db = MysqlServer(DATABASES)
        sql = "delete from node where ip='%s';" % node_ip
        ret = db.run_sql(sql)
        db.close()
        return ret\

    @staticmethod
    def update_node(node_data):
        db = MysqlServer(DATABASES)
        sql1 = "select nid from node where name='%s' and ip='%s';" % (node_data['node_name'], node_data['node_ip'])
        nid = db.run_sql(sql1)[0][0]
        sql2 = "update node set `name`='%s', `ip`='%s', `port`='%s', `cpus`='%s', `mem`='%s', `images`='%s', " \
              "`state`='%s', `containers`='%s', `os_version`='%s', `kernel_version`='%s', `docker_version`='%s', " \
              "`node_group_id`='%s', `user_group_id`='%s' where nid='%s';" % (node_data['node_name'],
                                                                              node_data['node_ip'],
                                                                              node_data['node_port'],
                                                                              node_data['node_cpus'],
                                                                              node_data['node_mem'],
                                                                              node_data['node_imgs'],
                                                                              node_data['node_state'],
                                                                              node_data['node_cons'],
                                                                              node_data['node_os'],
                                                                              node_data['node_ks'],
                                                                              node_data['node_ds'],
                                                                              node_data['node_group'],
                                                                              node_data['user_group'],
                                                                              nid )
        ret = db.run_sql(sql2)
        db.close()
        return ret


