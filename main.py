# -*- coding: utf-8 -*-
__author__ = 'CQ'

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from settings import settings
from url.urls import urls

from tornado.options import define, options, parse_command_line
define("port", default=8888, help="run on the given port", type=int)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


if __name__ == "__main__":
    app = tornado.web.Application(
        handlers=urls,
        **settings,
    )
    parse_command_line()
    print('The service is already running on port %s ...' % options.port)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
