# -*- coding: utf-8 -*-
__author__ = 'CQ'
import time
from handler.base import Base
import tornado.web
import threading
from model.node import NodeInfo
from model.data_format import DataManage
from myswarm import Myswarm
from settings import PRIVATE_REGISTRY
from settings import template_variables
import json
import uuid
from container_config import json_data
from settings import COOKIE_NAME


def prepare_data(username):
    node_group_id, user_group_id = NodeInfo.user_access(username)[0]
    node_list = NodeInfo.node_list(node_group_id, user_group_id)  # (((ip,port),(ip,port)))
    myswarm = Myswarm()
    image_data = list()
    ip_list = list()
    for ip, port in node_list:
        img_data = myswarm.show_images(ip, port)
        if image_data is None:  # 当节点不能连接时，避免报错，但不能消除等待连接超时
            continue
        image_data.append(dict())
        image_data[-1]['name'] = ip
        ip_list.append(ip)
        format_data = DataManage.image_list(img_data)  # 列表套字典的形式
        image_data[-1]['value'] = len(format_data)

    return image_data, ip_list


class Main(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_secure_cookie(COOKIE_NAME).decode()
        image_data, ip_list = prepare_data(username)
        self.render('main.html', image_data=json.dumps(image_data), ip_list=json.dumps(ip_list))


class NodeManage(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        threads = []
        node_update = threading.Thread(target=self._update_node)
        threads.append(node_update)
        node_pass = threading.Thread(target=self._get_pass)
        threads.append(node_pass)
        for t in threads:
            t.setDaemon(True)
            t.start()
        node_data = NodeInfo.node_info()
        node_data_handled = DataManage.manage_node_info(node_data)
        self.render("node/node_list.html", node_data=node_data_handled)

    def _update_node(self):
        pass
        # node_data = NodeInfo.node_info()
        # myswarm = Myswarm()
        # for line in node_data:
        #     node_ip = line[2]
        #     node_port = line[3]
        #     if myswarm.ping_port(node_ip, node_port) == 1:
        #         continue
        #     else:
        #         node_info = myswarm.node_list(node_ip, node_port)
        #         NodeInfo.node_info_update(node_info, node_ip)

    def _get_pass(self):
        pass


class ContList(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        get_all_node = self.get_argument('get_all_node', None)
        if node_ip is None and get_all_node is None:
            self.write("Something Wrong")
            return
        elif get_all_node:
            """
            直接点击Director中的Container查看所有容器管理时
            """
            node_list = NodeInfo.get_all_node()  # ((127.0.0.1, ), (192.168.180.128, ))
            myswarm = Myswarm()
            con_data_list = list()
            ip_list = list()
            for ip in node_list:
                node_ip = ip[0]
                ip_list.append(node_ip)
                node_port = NodeInfo.get_node_port(node_ip)[0][0]
                con_data_list.append([ip[0], myswarm.container_list(node_ip, node_port)])
            self.render('node/cont_list.html', con_data=con_data_list, node_ip=ip_list)
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            con_data = myswarm.container_list(node_ip, node_port)
            self.render('node/node_add.html', con_data=con_data, node_ip=node_ip)


class NodeAdd(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        temp_list = NodeInfo.get_group_list()
        self.render('node/node_create.html', group_list=temp_list)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        node_name = self.get_argument("node_name", None)
        flag = True
        if node_name is None:
            flag = False
        node_ip = self.get_argument("node_ip", None)
        if node_ip is None:
            flag = False
        node_port = self.get_argument("node_port", None)
        if node_port is None:
            flag = False
        node_cpus = self.get_argument("node_cpus", None)
        if node_cpus is None:
            flag = False
        node_mem = self.get_argument("node_mem", None)
        if node_mem is None:
            flag = False
        node_imgs = self.get_argument("node_imgs", None)
        if node_imgs is None:
            flag = False
        node_cons = self.get_argument("node_cons", None)
        if node_cons is None:
            flag = False
        node_state = self.get_argument("node_state", None)
        if node_state is None:
            flag = False
        node_os = self.get_argument("node_os", None)
        if node_os is None:
            flag = False
        node_ks = self.get_argument("node_ks", None)
        if node_ks is None:
            flag = False
        node_ds = self.get_argument("node_ds", None)
        if node_ds is None:
            flag = False
        node_ds = self.get_argument("node_ds", None)
        if node_ds is None:
            flag = False
        node_group = self.get_argument("node_group", None)
        if node_group is None:
            flag = False
        user_group = self.get_argument("user_group", None)
        print(user_group)
        print(type(user_group))
        if user_group is None:
            flag = False
            print(user_group)
        if not flag:
            self.write("Sorry you submitted the data incorrectly ...")
            return
        node_dict = dict()
        node_dict['node_name'] = node_name
        node_dict['node_ip'] = node_ip
        node_dict['node_port'] = node_port
        node_dict['node_cpus'] = node_cpus
        node_dict['node_mem'] = node_mem
        node_dict['node_imgs'] = node_imgs
        node_dict['node_cons'] = node_cons
        node_dict['node_state'] = node_state
        node_dict['node_os'] = node_os
        node_dict['node_ks'] = node_ks
        node_dict['node_ds'] = node_ds
        node_dict['node_group'] = node_group
        node_dict['user_group'] = user_group  # 默认管理员组
        print(node_dict)
        save_status = NodeInfo.save_node(node_dict)
        self.redirect("/nodemanage?active=2&save_status=True")


class NodeModify(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        action = self.get_argument('action', None)
        if node_ip is None or action is None:
            self.redirect("/nodemanage?active=2")
        elif action == "delete":
            del_status = NodeInfo.delete_node(node_ip)
            self.redirect("/nodemanage?active=2&del_status=True")
        elif action == "update":
            update_dict = dict()
            update_dict['node_ip'] = self.get_argument('node_ip', None)
            update_dict['node_name'] = self.get_argument('node_name', None)
            update_dict['node_port'] = self.get_argument('node_port', None)
            update_dict['node_cpus'] = self.get_argument('node_cpus', None)
            update_dict['node_mem'] = self.get_argument('node_mem', None)
            update_dict['node_imgs'] = self.get_argument('node_imgs', None)
            update_dict['node_state'] = self.get_argument('node_state', None)
            update_dict['node_cons'] = self.get_argument('node_cons', None)
            update_dict['node_os'] = self.get_argument('node_os', None)
            update_dict['node_ks'] = self.get_argument('node_ks', None)
            update_dict['node_ds'] = self.get_argument('node_ds', None)
            update_dict['node_group'] = self.get_argument('node_group', None)  #node_group获取是的它的ID值
            update_dict['user_group'] = self.get_argument('user_group', None)  #user_group获取是的它的ID值
            temp_list = NodeInfo.get_group_list()
            self.render("node/node_modify.html", node_data=update_dict, group_list=temp_list)

    def post(self, *args, **kwargs):
        action = self.get_argument('action', None)
        if action is None:
            self.write("Sorry you submitted the data incorrectly ...")
        elif action == 'update':
            update_dict = dict()
            update_dict['node_ip'] = self.get_argument('node_ip', None)
            update_dict['node_name'] = self.get_argument('node_name', None)
            update_dict['node_port'] = self.get_argument('node_port', None)
            update_dict['node_cpus'] = self.get_argument('node_cpus', None)
            update_dict['node_mem'] = self.get_argument('node_mem', None)
            update_dict['node_imgs'] = self.get_argument('node_imgs', None)
            update_dict['node_state'] = self.get_argument('node_state', None)
            update_dict['node_cons'] = self.get_argument('node_cons', None)
            update_dict['node_os'] = self.get_argument('node_os', None)
            update_dict['node_ks'] = self.get_argument('node_ks', None)
            update_dict['node_ds'] = self.get_argument('node_ds', None)
            update_dict['node_group_id'] = self.get_argument('node_group_id', None)
            update_dict['node_group'] = self.get_argument('node_group', None)
            update_dict['user_group_id'] = self.get_argument('user_group_id', None)
            update_dict['user_group'] = self.get_argument('user_group', None)
            upd_status = NodeInfo.update_node(update_dict)
            self.redirect("/nodemanage?active=2&update_status=True")


class ContHandele(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip')
        con_id = self.get_argument('con_id')

        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        myswarm = Myswarm()
        con_data_handled = myswarm.container_info(node_ip, node_port, con_id)
        self.render("node/cont_handle.html", name=template_variables, node_ip=node_ip,
                    node_port=node_port, con_id=con_id, con_data=con_data_handled)


class ContStart(Base):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)

        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        print("      Starting the container......")
        ret = myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.redirect("/contlist?active=3&get_all_node=True")


class ContStop(Base):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.redirect("/contlist?active=3&get_all_node=True")


class ContRestart(Base):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)

        container_ip = {}
        myswarm = Myswarm()
        if not con_dict['con_id']:
            self.write("There is no container id")
        myswarm.stop_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        time.sleep(2)
        myswarm.start_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.redirect("/contlist?active=3&get_all_node=True")


class ContDestroy(Base):
    @tornado.web.authenticated
    def get(self, *args, **kargs):
        con_dict = {}
        for key in ['node_ip', 'port', 'con_id']:
            con_dict[key] = self.get_argument(key)
        myswarm = Myswarm()
        myswarm.destroy_container(con_dict['node_ip'], con_dict['port'], con_dict['con_id'])
        self.redirect("/contlist?active=3&get_all_node=True")


class ContCreate(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument('node_ip', None)
        if node_ip is None:
            self.write("Something Wrong")
            return
        else:
            node_port = NodeInfo.get_node_port(node_ip)[0][0]
            myswarm = Myswarm()
            images_data = myswarm.images_list(node_ip, node_port)
            self.render('node/cont_create.html', node_ip=node_ip, images=images_data)

    def post(self, *args, **kwargs):
        json_ret = json.loads(json_data[0])
        node_ip = self.get_argument('node_ip', 'None')
        if node_ip == 'None':
            print("There is no node ip")
            return
        port_ret = NodeInfo.get_node_port(node_ip)
        if len(port_ret) < 1:
            print("There is no port of the node")
            return
        else:
            node_port = port_ret[0][0]

        con_dict = {}
        for key in ['Cmd', 'Image', 'CpuPeriod', 'CpuQuota', 'CpuShares', 'Memory']:
            con_dict[key] = self.get_argument(key.lower())
            if key == 'Cmd' and con_dict[key] != "":
                json_ret[key] = con_dict[key].split()
            elif key == 'Image' and con_dict[key] != "":
                json_ret[key] = con_dict[key]
            elif con_dict[key] != "":
                json_ret['HostConfig'][key] = int(con_dict[key])

        myswarm = Myswarm()
        json_ret['Name'] = str(uuid.uuid4())[0:13]
        json_ret['Hostname'] = json_ret['Name']

        container_id = myswarm.create_container(node_ip, node_port, json_ret)
        if not container_id:
            print("Can not create the Container")
            return
        ret = myswarm.start_container(node_ip, node_port, container_id)
        self.redirect("/contlist?active=3&get_all_node=True&res=%s" % ret)


class ImgList(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_secure_cookie(COOKIE_NAME).decode()
        node_group_id, user_group_id = NodeInfo.user_access(username)[0]
        node_list = NodeInfo.node_list(node_group_id, user_group_id)  # (((ip,port),(ip,port)))
        myswarm = Myswarm()
        image_data = list()
        for ip,port in node_list:
            image_data.append(dict())
            image_data[-1]['node_ip'] = ip
            image_data[-1]['node_port'] = port
            img_data = myswarm.show_images(ip,port)
            if img_data is None:  # 测试数据时会添加不存在的节点，避免出错，但不能避免连接超时等待
                image_data.pop()
                continue
            format_data = DataManage.image_list(img_data)  # 列表套字典的形式
            image_data[-1]['images'] = format_data
        self.render('node/image_list.html', image_data=image_data ,node_ip=node_list)


class ImgModify(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        action = self.get_argument('action', None)
        node_ip = self.get_argument('node_ip', None)
        node_port = self.get_argument('node_port', None)
        image_id = self.get_argument('image_id', None)
        if node_ip is None or node_port is None or image_id is None or action is None:
            self.write("Sorry you submitted the data incorrectly ...")
        myswarm = Myswarm()
        if action == "delete":
            res = myswarm.remove_images(node_ip, node_port, image_id)
            self.redirect("/imglist?active=4&delete_status=True")
        elif action == "detail":
            res = myswarm.detail_image(node_ip, node_port, image_id)
            self.render("node/image_detail.html", detail_data = res)


class ImgPull(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        node_ip = self.get_argument("node_ip")
        node_port = NodeInfo.get_node_port(node_ip)[0][0]
        self.render('node/image_pull.html', node_ip=node_ip, node_port=node_port, search_data=dict())

    def post(self, *args, **kwargs):
        node_ip = self.get_argument("node_ip", None)
        node_port = self.get_argument("node_port", None)
        action = self.get_argument("action", None)
        myswarm = Myswarm()
        if action == "search":
            search_content = self.get_argument("search_content", None)
            res = myswarm.search_image(node_ip, node_port, search_content)
            search_data = DataManage.search_images_list(res)
            self.render("node/image_pull.html", node_ip=node_ip, node_port=node_port, search_data=search_data)
        elif action == "pull":
            pull_name = self.get_argument("pull_name", None)
            res = myswarm.pull_image(node_ip, node_port, pull_name)


class ImgPush(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        push_list = self.get_argument('push_list', None)
        push_list = json.loads(push_list)
        push_list = DataManage.push_image_list(push_list)
        json_list = json.dumps(push_list)
        self.render("node/image_push.html", push_list=push_list , json_list=json_list)

    def post(self, *args, **kwargs):
        registry_name = self.get_argument("registry_name", None)
        registry_port = self.get_argument("registry_port", None)
        push_list = self.get_argument("push_list", None)
        push_list = json.loads(push_list)
        myswarm = Myswarm()
        print(push_list)
        for row in push_list:
            # ip, port, push_name, registry_ip, registry_port, registry_img_name, tag
            thr = threading.Thread(target=myswarm.push_image, args=(row[1], row[2], row[3], registry_name,
                                                                    registry_port,row[4], row[5]))
            thr.start()
        self.redirect('/imglist?active=4')

class ContRemotion(Base):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        pass

    def post(self):
        remotion_data = self.get_argument("remotion_data", None)
        remotion_data = json.loads(remotion_data)
        des_ip = remotion_data[0]
        des_port = NodeInfo.get_node_port(des_ip)[0][0]
        myswarm = Myswarm()
        for row in remotion_data[1:]:
            if des_ip == row[0]:
                continue
            conf_dict = dict()
            src_ip = str(row[0])
            src_port = NodeInfo.get_node_port(src_ip)[0][0]
            cont_id = row[1]
            cont_name = row[2]
            temp = myswarm.detail_container(src_ip, src_port, cont_id)
            conf_dict['OpenStdin'] = temp['Config']['OpenStdin']
            conf_dict['Tty'] = temp['Config']['Tty']
            conf_dict['Cmd'] = temp['Config']['Cmd']
            conf_dict['Image'] = PRIVATE_REGISTRY + cont_name
            conf_dict['Name'] = cont_name
            conf_dict['Hostname'] = cont_name.replace("/","")
            conf_dict['HostConfig'] = dict()
            conf_dict['HostConfig']['CpuPeriod'] = temp['HostConfig']['CpuPeriod']
            conf_dict['HostConfig']['CpuQuota'] = temp['HostConfig']['CpuQuota']
            conf_dict['HostConfig']['CpuShares'] = temp['HostConfig']['CpuShares']
            conf_dict['HostConfig']['Memory'] = temp['HostConfig']['Memory']
            thr = threading.Thread(target=myswarm.remotion_container,args=(
                src_ip, src_port , cont_id, cont_name, des_ip, des_port, conf_dict
            ))
            thr.start()


