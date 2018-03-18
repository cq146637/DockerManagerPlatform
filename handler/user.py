# -*- coding: utf-8 -*-
__author__ = 'CQ'
import tornado.web
from .base import Base
from settings import COOKIE_NAME
from model.check import Check
from .node import prepare_data
import json


class Login(Base):

    def get(self, *args, **kwargs):
        self.render("login.html", login_strings=dict(username="Username", password="Password"))

    def post(self, *args, **kwargs):
        input_username = self.get_argument("username")
        input_password = self.get_argument("password")
        check_result = Check.login_check(input_username, input_password)
        if check_result == "Invalid username":
            self.render("login.html", login_strings=dict(username="Invalid username", password="Password"))
        elif check_result == "Incorrect password":
            self.render("login.html", login_strings=dict(username="Username", password="Incorrect password"))
        elif check_result == "admin":
            self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)
            self.redirect("/main")
        else:
            self.set_secure_cookie(COOKIE_NAME, input_username, expires_days=1)
            self.redirect("login.html")


class Welcome(Base):
    @tornado.web.authenticated  # tornado Web自身提供，没有登录时，自动跳转到登录界面，做身份验证用的
    def get(self):
        username = self.get_secure_cookie(COOKIE_NAME).decode()
        image_data, ip_list = prepare_data(username)
        self.render('main.html', image_data=json.dumps(image_data),
                    ip_list=json.dumps(ip_list), username=self.current_user)


class Logout(Base):
    def get(self, *args, **kwargs):
        self.clear_cookie(COOKIE_NAME)
        self.write("<script language='javascript'>top.window.location.href='/';</script>")
