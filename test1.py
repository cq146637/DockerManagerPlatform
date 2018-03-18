# -*- coding: utf-8 -*-
__author__ = 'CQ'
import docker
from settings import PRIVATE_REGISTRY

"""
1. docker commit 180b966c3335 192.168.180.128:5000/wode/darksheer/ubuntu

    sha256:fa1624a6a07786ef00485a58b5e1b121d6747749c111bc6bfe37679f7d87dd93

2. docker tag fa1624a6a07786ef00485a58b5e1 192.168.180.128:5000/wode/darksheer/ubuntu:v1.2.3

3. docker push 192.168.180.128:5000/wode/darksheer/ubuntu:v1.2.3

4. curl http://192.168.180.128:5000/v2/_catalog

"""


def main():
    client_ins = docker.Client(base_url='tcp://' + '192.168.180.128' + ":" + '2375', version='1.20', timeout=5)
    # image_id = client_ins.commit("180b966c3335",repository="192.168.180.128:5000/remotion/darksheer/ubuntu_2")['Id'].split(":")[1]
    # res = client_ins.tag(image_id, "192.168.180.128:5000/remotion/darksheer/ubuntu_2")
    # res = client_ins.push("192.168.180.128:5000/remotion/darksheer/ubuntu_2")
    res = client_ins.remove_image("192.168.180.128:5000/5353be20-6100")
    print(PRIVATE_REGISTRY)
    # stop_container
    # client_ins_1 = docker.Client(base_url='tcp://' + '192.168.180.130' + ":" + '2375', version='1.20', timeout=5)
    # res = client_ins_1.pull("192.168.180.128:5000/remotion/darksheer/ubuntu_2")
    # create_container
    return res




print(main())