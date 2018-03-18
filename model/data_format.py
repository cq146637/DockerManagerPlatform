# -*- coding: utf-8 -*-
__author__ = 'CQ'
class DataManage(object):
    @staticmethod
    def manage_node_info(result):
        node_data = dict()
        num = 1
        for line in result:
            tmp_dict = dict()
            tmp_dict["name"] = line[1]
            tmp_dict["node_ip"] = line[2]
            tmp_dict["port"] = line[3]
            tmp_dict["cpus"] = line[4]
            tmp_dict["mem"] = line[5]
            tmp_dict["images"] = line[6]
            tmp_dict["state"] = line[7]
            tmp_dict["containers"] = line[8]
            tmp_dict["os_version"] = line[9]
            tmp_dict["kernel_version"] = line[10]
            tmp_dict["docker_version"] = line[11]
            tmp_dict["node_group_id"] = line[12]
            tmp_dict["user_group_id"] = line[13]
            tmp_dict["node_group"] = line[14]
            tmp_dict["user_group"] = line[15]
            node_data[num] = tmp_dict
            num += 1
        return node_data

    @staticmethod
    def group_list(result):
        group_data = []
        num = 1
        for line in result:
            tmp_dic = {}
            if num < 10:
                tmp_dic['id'] = "0" + str(num)
            else:
                tmp_dic['id'] = str(num)
            tmp_dic['name'] = line[0]
            tmp_dic['isParent'] = "true"
            tmp_dic['target'] = "rightFrame"
            tmp_dic['url'] = "group?group_id=" + tmp_dic['id']
            group_data.append(tmp_dic)
            num += 1
        return group_data

    @staticmethod
    def node_list(result, id, name):
        node_data = []
        num = 1
        for line in result:
            tmp_dic = {}
            if num < 10:
                tmp_dic['id'] = id + "0" + str(num)
            else:
                tmp_dic['id'] = id + str(num)
            tmp_dic['name'] = line[0]
            tmp_dic['isParent'] = "false"
            tmp_dic['target'] = "rightFrame"
            tmp_dic['url'] = "node?node_ip=" + tmp_dic['name']
            node_data.append(tmp_dic)
            num += 1
        return node_data

    @staticmethod
    def manage_con_usage_info(result):
        dict_data = {}
        num = 1
        for line in result:
            tmp_dict = dict()
            tmp_dict["con_id"] = line[0]
            tmp_dict["con_ip"] = line[1]
            tmp_dict["node_ip"] = line[2]
            tmp_dict["user_name"] = line[3]
            tmp_dict["con_app"] = line[4]
            tmp_dict["con_desc"] = line[5]
            dict_data[num] = tmp_dict
            num += 1
        return dict_data

    @staticmethod
    def image_list(image_data):
        import time
        import re
        data_list = list()
        index = 1
        for data in image_data:
            data_list.append(dict())
            data_list[-1]['id'] = index
            data_list[-1]['Created'] = time.ctime(data['Created'])
            data_list[-1]['Labels'] = data['Labels']
            data_list[-1]['Id'] = data['Id'].split(':')[1]
            if data['RepoTags'] is None:
                data_list[-1]['RepoTags'] = None
                data_list[-1]['Tags'] = None
            elif len(re.findall(":", data['RepoTags'][0])) == 2:
                li = data['RepoTags'][0].split(":")
                data_list[-1]['RepoTags'] = li[0] + ':' + li[1]
                data_list[-1]['Tags'] = data['RepoTags'][0].split(":")[2]
            else:
                data_list[-1]['RepoTags'] = data['RepoTags'][0].split(":")[0]
                data_list[-1]['Tags'] = data['RepoTags'][0].split(":")[1]
            data_list[-1]['Size'] = data['Size']
            index += 1
        return data_list

    @staticmethod
    def search_images_list(search_data):
        data_list = list()
        index = 1
        for row in search_data:
            data_row = list()
            data_row.append(index)
            data_row.append(row)
            data_list.append(data_row)
            index += 1
        return data_list\

    @staticmethod
    def push_image_list(push_list):
        # 格式：[序号，IP，PORT，REGISTRY_NAME,TAG]
        data_list = list()
        index = 1
        for row in push_list:
            data_row = list()
            data_row.append(index)
            data_row.extend(row[0:2])
            data_row.append(row[2])
            data_row.append( '/'.join(row[2].split("/")[1:]))
            data_row.append(row[3])
            data_list.append(data_row)
            index += 1
        return data_list
