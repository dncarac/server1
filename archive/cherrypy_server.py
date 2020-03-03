#!/usr/bin/env python
# coding: utf-8
''' src.cherrypy_server --

@summary: module_summary

@description: module_detailed_description

__Created__ = "2019-04-11"
__Updated__ = "2019-04-11"

@author: Den
@copyright: Copyright © 2019 Den
@license: ALL RIGHTS RESERVED
'''
import cherrypy


class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        return "Hello world!"


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
