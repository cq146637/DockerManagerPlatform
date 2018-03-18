# -*- coding: utf-8 -*-
__author__ = 'CQ'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import os
import json


from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("username")  # 将用户cookie解密在把值返回


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated  # tornado Web自身提供，没有登录时，自动跳转到登录界面，做身份验证用的
    def get(self):
        self.render("welcome.html", username=self.current_user)


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("username")
        self.redirect("/")


if __name__ == "__main__":
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        # cookie不会以明文存储在客户端，而是用此字符串加密cookie，然后才存储在客户端
        "cookie_secret": "AQAAALudVkKt/AYA0bLPykwXoIBRVYTO",
        # 当用户没有登录时，tornado会自动跳转的登录URL请求用户登录
        "login_url": "/login"
    }
    urls = [
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/test', WelcomeHandler),
        (r'/logout', LogoutHandler)
    ]

    app = tornado.web.Application(
        handlers=urls,
        **settings,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
