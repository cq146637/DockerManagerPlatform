# -*- coding: utf-8 -*-
__author__ = 'CQ'
import docker
import socket
import time
import requests
import threading
from curl import Curl
from model.node import NodeInfo
from settings import PRIVATE_REGISTRY


class Myswarm(object):

    def ping_port(self, ip, port):
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.settimeout(0.2)
        address = (str(ip), int(port))
        try:
            cs.connect((address))
        except socket.error as e:
            print(e)
            return 1
        cs.close()
        return 0

    def insert_con_usage(self, node_ip, container_ip, container_id):
        pass
        # if not container_id:
        #     return
        # else:
        #     NodeInfo.insert_con_usage(container_id, container_ip, node_ip)

    def delete_con_usage(self, container_id):
        pass
        # if not container_id:
        #     return
        # else:
        #     NodeInfo.delete_con_usage(container_id)

    def _container_detail(self, node_ip, node_port, containers_id):
        url = ('http://' + node_ip + ":" + node_port + "/containers/" + containers_id + "/json")
        container_more_url = Curl(url)
        ret_json = container_more_url.get_value()
        return ret_json

    def container_list(self, node_ip, node_port):
        url = 'http://' + node_ip + ":" + node_port + "/containers/json?all=1"
        container_url = Curl(url)
        ret_json = container_url.get_value()
        con_data = {}
        container_id = []
        if ret_json:
            for i in ret_json:
                container_id.append(i['Id'][0:12])
        else:
            return con_data

        if len(container_id) < 1:
            return con_data
        else:
            con_data = {}
            con_num = 1
            for con_id in container_id:
                tmp_dict = {}
                ret_json = self._container_detail(node_ip, node_port, con_id)
                if len(ret_json) < 1:
                    return con_data
                if ('Running' in ret_json['State'].keys()) and (
                    'Status' not in ret_json['State'].keys()):  # for docker 1.7
                    con_state = str(ret_json['State']['Running'])
                elif 'Status' in ret_json['State'].keys():  # for docker 1.9 and higher
                    con_state = str(ret_json['State']['Status'])
                else:  # for else
                    con_state = "Exited"
                tmp_dict['id_num'] = ret_json['Id'][0:12]
                tmp_dict['con_ip'] = ret_json['NetworkSettings']['IPAddress']
                tmp_dict['name'] = ret_json['Name']
                tmp_dict['cpuperiod'] = ret_json['HostConfig']['CpuPeriod']
                tmp_dict['cpuquota'] = ret_json['HostConfig']['CpuQuota']
                tmp_dict['memory'] = ret_json['HostConfig']['Memory']
                tmp_dict['state'] = con_state
                tmp_dict['cmd'] = str(ret_json['Config']['Cmd'])
                tmp_dict['created'] = ret_json['State']['StartedAt']
                con_data[con_num] = tmp_dict
                con_num += 1
        return con_data

    def images_list(self, node_ip, node_port):
        client_ins = docker.Client(base_url='tcp://' + node_ip + ':'
                                            + node_port, version='1.20', timeout=5)
        ret_json = client_ins.images()
        images_list = []
        for one in ret_json:
            images_list.append(one['RepoTags'])
        return images_list

    def create_container(self, node_ip, node_port, conf):
        client_ins = docker.Client(base_url='tcp://' + node_ip + ":" + node_port, version='1.20', timeout=5)
        print("      Create the container......")
        container_ret = client_ins.create_container(image=conf['Image'],
                                                    stdin_open=conf['OpenStdin'],
                                                    tty=conf['Tty'],
                                                    command=conf['Cmd'],
                                                    name=conf['Name'],
                                                    hostname=conf['Hostname'],
                                                    host_config=conf['HostConfig'])
        if container_ret:
            time.sleep(0.3)
            return (container_ret['Id'])
        else:
            print("Can not create container")
            return

    def start_container(self, node_ip, node_port, container_id):
        if len(container_id) > 0:
            container_ip = ""
            client_ins = docker.Client(base_url='tcp://' + node_ip + ":" + node_port, version='1.20', timeout=5)
            client_ins.start(container_id)
            time.sleep(0.5)
            con_info = self._container_detail(node_ip, node_port, container_id)
            self.insert_con_usage(node_ip, con_info['NetworkSettings']['IPAddress'], container_id[0:12])
        else:
            print("Please enter the Container ID")
            return

    def container_info(self, node_ip, node_port, container_id):
        con_data = {}
        tmp_dict = {}
        ip_ret = ""
        ret_json = self._container_detail(node_ip, node_port, container_id)
        if len(ret_json) < 1:
            return con_data

        con_state = ""
        if ('Running' in ret_json['State'].keys()) and ('Status' not in ret_json['State'].keys()):  # for docker 1.7
            con_state = str(ret_json['State']['Running'])
        elif 'Status' in ret_json['State'].keys():  # for docker 1.9 and higher
            con_state = str(ret_json['State']['Status'])
        else:  # for else
            con_state = "Exited"
        tmp_dict['id_num'] = ret_json['Id'][0:12]
        tmp_dict['node_ip'] = node_ip
        tmp_dict['con_ip'] = ret_json['NetworkSettings']['IPAddress']
        tmp_dict['name'] = ret_json['Name']
        tmp_dict['image'] = ret_json['Image']
        tmp_dict['created'] = ret_json['State']['StartedAt']
        tmp_dict['state'] = con_state
        tmp_dict['memory'] = ret_json['HostConfig']['Memory']
        tmp_dict['cpuperiod'] = ret_json['HostConfig']['CpuPeriod']
        tmp_dict['cpuquota'] = ret_json['HostConfig']['CpuQuota']
        tmp_dict['hostname'] = str(ret_json['Config']['Hostname'])
        tmp_dict['cmd'] = str(ret_json['Config']['Cmd'])
        con_data[1] = tmp_dict
        return con_data

    def stop_container(self, node_ip, node_port, container_id):
        if len(container_id) > 0:
            print("      Stop the container %s ........" % container_id)
            client_ins = docker.Client(base_url='tcp://' + node_ip + ":"
                                                + node_port, version='1.20', timeout=5)
            client_ins.stop(container_id)
        else:
            print("Please enter the Container ID")
            return

    def destroy_container(self, node_ip, node_port, container_id):
        if len(container_id) > 0:
            print("      Destroy the container %s ....... " % container_id)
            client_ins = docker.Client(base_url='tcp://' + node_ip + ':'
                                                + node_port, version='1.20', timeout=5)
            try:
                client_ins.stop(container_id)
                time.sleep(0.3)
                client_ins.remove_container(container_id)
                time.sleep(0.3)
            except docker.errors.NotFound:
                print("      NO Such container id")
            self.delete_con_usage(container_id)
        else:
            print("Please enter the Container ID")
            return 1

    def detail_container(self, node_ip, node_port, container_id):
        client_ins = docker.Client(base_url='tcp://' + node_ip + ':' + node_port, version='1.20', timeout=5)
        res = client_ins.inspect_container(container_id)
        return res

    def show_images(self, node_ip, node_port):
        try:
            client_ins = docker.Client(base_url='tcp://' + node_ip + ":" + node_port, version='1.20', timeout=5)
            res = client_ins.images()
        except requests.exceptions.ConnectTimeout:
            res = None
        return res

    def remove_images(self, ip, port, id):
        client_ins = docker.Client(base_url='tcp://' + ip + ":" + port, version='1.20', timeout=5)
        res = client_ins.remove_image(id)
        return res

    def detail_image(self, ip, port, id):
        client_ins = docker.Client(base_url='tcp://' + ip + ":" + port, version='1.20', timeout=5)
        res = client_ins.inspect_image(id)
        return res

    def search_image(self, ip, port, search_content):
        client_ins = docker.Client(base_url='tcp://' + ip + ":" + port, version='1.20', timeout=5)
        res = client_ins.search(search_content)
        return res

    def pull_image(self, ip, port, pull_name):
        client_ins = docker.Client(base_url='tcp://' + ip + ":" + port, version='1.20', timeout=5)
        res = client_ins.pull(pull_name)
        return res

    def push_image(self, ip, port, push_name, registry_ip, registry_port, registry_img_name, tag):
        client_ins = docker.Client(base_url='tcp://' + ip + ":" + port, version='1.20', timeout=5)
        client_ins.tag(push_name, registry_ip + ":" + registry_port + '/' + registry_img_name, tag=tag)
        res = client_ins.push(registry_ip + ":" + registry_port + '/' + registry_img_name + ':' + tag)
        return res

    def remotion_container(self, src_ip, src_port, cont_id, cont_name, des_ip, des_port, conf):
        client_ins = docker.Client(base_url='tcp://' + src_ip + ":" + src_port, version='1.20', timeout=5)
        image_id = client_ins.commit(cont_id, repository=PRIVATE_REGISTRY + cont_name)['Id'].split(":")[1]
        res = client_ins.tag(image_id, repository=PRIVATE_REGISTRY + cont_name)
        res = client_ins.push(repository=PRIVATE_REGISTRY + cont_name)
        thr_1 = threading.Thread(target=client_ins.remove_image, args=(PRIVATE_REGISTRY + cont_name,))
        thr_2 = threading.Thread(target=self.stop_container, args=(src_port, src_port, cont_id))
        client_ins_1 = docker.Client(base_url='tcp://' + des_ip + ":" + des_port, version='1.20', timeout=5)
        res = client_ins_1.pull(PRIVATE_REGISTRY + cont_name)
        _cont_id = self.create_container(des_ip, des_port, conf)
        res = self.start_container(des_ip, des_port, _cont_id)
        thr_1.start()
        thr_2 .start()
        return res


