# -*- coding: utf-8 -*-
__author__ = 'CQ'
from sqlalchemy import create_engine, text, update, Table
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine('mysql://docker:123456@192.168.180.128:3306/docker?charset=utf8',
                       encoding="utf-8", pool_size=1000, pool_recycle=3600, echo=False)

Base = declarative_base()


class Node(Base):

    __tablename__ = 'node'
    nid = Column(Integer, primary_key=True, autoincrement=True)  # ID号
    name = Column(String(32))  # 节点名
    ip = Column(String(32))  # 节点ip
    port = Column(String(32))  # 节点端口
    cpus = Column(String(32))  # 节点CPU个数
    mem = Column(String(32))  # 节点内存大小
    images = Column(String(32))  # 节点镜像数
    state = Column(String(32))  # 节点当前状态
    containers = Column(String(32))  # 节点上的容器数
    os_version = Column(String(32))  # 节点操作系统版本
    kernel_version = Column(String(32))  # 节点内核版本
    docker_version = Column(String(32))  # 节点docker版本
    node_group_id = Column(Integer, ForeignKey('node_group.gid', ondelete="CASCADE"))  # 节点所属组群
    node_group = relationship("NodeGroup", backref='node')
    user_group_id = Column(Integer, ForeignKey('user_group.gid', ondelete="CASCADE"))  # 节点所属管理组
    user_group = relationship("UserGroup", backref='user')

    def __repr__(self):
        return "<Node(name = '%s', ip = '%s', port = '%s', cpus = '%s', mem = '%s', images = '%s', state = '%s'" \
               ", node_group = '%s', user_group = '%s', container = '%s', os_version = '%s', kernel_version = '%s', " \
               "docker_version = '%s')>" % (self.name,
                                            self.ip,
                                            self.port,
                                            self.cpus,
                                            self.mem,
                                            self.images,
                                            self.state,
                                            self.node_group.caption,
                                            self.user_group.caption,
                                            self.containers,
                                            self.os_version,
                                            self.kernel_version,
                                            self.docker_version
                                            )


class NodeGroup(Base):

    __tablename__ = 'node_group'
    gid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    caption = Column(String(32))
    user_group_id = Column(Integer, ForeignKey('user_group.gid', ondelete="CASCADE"))  # 节点组所属组群
    user_group = relationship("UserGroup", backref='user')

    def __repr__(self):
        return "<NodeGroup(name = %s, caption = %s, manager_group = %s)>" % (self.name,
                                                                             self.caption,
                                                                             self.user_group.caption)


class Container(Base):

    __tablename__ = 'container'
    cid = Column(Integer, primary_key=True)  # 主键自增ID
    con_id = Column(String(64))  # 容器ID
    con_addr = Column(String(32))  # 容器IP
    node_id = Column(Integer, ForeignKey('node.nid', ondelete="CASCADE"))  # 容器所属节点
    node = relationship("Node", backref='container')
    user_name = Column(String(32))  # 运行容器用户名
    con_app = Column(String(32))  # 容器上运行的应用
    con_desc = Column(String(256))   # 容器用途描述

    def __repr__(self):
        return "<Container(con_id = %s, con_addr = %s, node_ip = %s, user_name = %s, con_app = %s , con_desc = %s)>" % \
               (self.con_id, self.con_addr, self.node.ip, self.user_name, self.con_app, self.con_desc)


class User(Base):

    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))  # 用户名
    password = Column(String(128))  # 用户密码
    user_group_id = Column(Integer, ForeignKey('user_group.gid', ondelete="CASCADE"))  # 用户所属组群
    user_group = relationship("UserGroup", backref='user')

    def __repr__(self):
        return "<user(name = %s, password = %s, user_group = %s)>" % (self.name, self.password, self.user_group.caption)


class UserGroup(Base):
    """
        用户组能定义用户权限以及管理节点组和节点
    """
    __tablename__ = 'user_group'
    gid = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(32))

    def __repr__(self):
        return "<UserGroup(caption = %s>" % self.caption


if __name__ == "__main__":
    Base.metadata.create_all(engine)


