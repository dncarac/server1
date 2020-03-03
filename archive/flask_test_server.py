#!/usr/bin/env python
# coding: utf-8
''' flask_test_server --

@summary: module_summary

@description: module_detailed_description

__Created__ = "2019-04-16"
__Updated__ = "2019-04-16"

@author: Den
@copyright: Copyright © 2019 Den
@License: ALL RIGHTS RESERVED
'''
from flask import Flask
flapp = Flask(__name__)


@flapp.route('/')
def hello_world():
    return '''
    <!DOCTYPE HTML>
<html>
<head>
<title>Title of the document</title>
</head>

<body>
'Hello, World!'
The content of the document......
</body>

</html>'Hello, World!
'''

