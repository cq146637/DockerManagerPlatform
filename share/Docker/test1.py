# -*- coding: utf-8 -*-
__author__ = 'CQ'

import docker


# def _container_list_more(self, node_ip, node_port ,container_id):
#     """
#         有些性能或监控相关的数据，在官方提供的接口中没有很好的实现
#         我们需要直接从Docker engine中获取数据，此时就可以使用Docker engine提供的原生Restful接口
#     :param self:
#     :param node_ip:
#     :param node_port:
#     :param container_id:
#     :return:
#     """
#     url = ('http://' + node_ip + ":" + node_port + "/containers/" + container_id + "/json")
#     container_more_url = Curl(url)
#     ret_json = container_more_url.get_value()
#     return ret_json


if __name__ == "__main__":
    client_ins = docker.Client(base_url='tcp://127.0.0.1:2357', version='1.20', timeout=10)

    print(" Create the container ... ")

    conf = {
        "Name": "/berserk_heisenberg-1",  # 名称要唯一
        "HostName": "/berserk_heisenberg-1",
        "Domainname": "",
        "User": "",
        "AttachStdin": True,
        "AttachStdout": True,
        "AttachStderr": True,
        "Tty": True,
        "OpenStdin": True,
        "StdinOnce": True,
        "Env": [
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        ],
        "Cmd": [
            "/bin/bash"
        ],
        "Image": "docker.io/holbertonschool/base-ubuntu-1404:latest",
        "Volumes": None,
        "WorkingDir": "",
        "Entrypoint": None,
        "OnBuild": None,
        "Labels": {}
    }

    container_ret = client_ins.create_container(image=conf['Image'],
                                                stdin_open=conf['OpenStdin'],
                                                tty=conf['Tty'],
                                                command=conf['Cmd'],
                                                name=conf['Name'],
                                                hostname=conf['Hostname'],
                                                host_config=conf['HostConfig']
                                                )

    client_ins.restart()
    client_ins.start()
    client_ins.stop()
    client_ins.unpause()
    client_ins.update_container()
    client_ins.wait()
