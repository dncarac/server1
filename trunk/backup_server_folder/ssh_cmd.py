#!/usr/bin/env python
# coding: utf-8
''' get_file_list.ssh_cmd --

@summary: 

@description: module_detailed_description

__Created__ = "2019-04-18"
__Updated__ = "2019-04-20"

@author: Den
@copyright: Copyright © 2019 Den
@License: ALL RIGHTS RESERVED
'''
from fabric import Connection

result = Connection('hostgator.com:2222').run('uname -s', hide=True)
msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
print(msg.format(result))
