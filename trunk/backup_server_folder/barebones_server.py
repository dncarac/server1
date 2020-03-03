#! ./venv/scripts/pythonw
# -*- coding: utf-8 -*-
'''
trunk.Scratch.backup_server_folder.backup_server_folder.py --

Server module for TypeLines!

Receives html requests from the client, receives transmitted information; generates responses, sends
responses back to client

__CreatedOn__="2018-04-02"
__UpdatedOn__="2020-01-12"

@author: Den
@copyright: Copyright © 2018-2019 Den
@license: ALL RIGHTS RESERVED
'''
from TaskData import TaskData
import bottle
import canister
from canister import session
from waitress import serve

bt_app = bottle.Bottle()
bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())


@bt_app.post('/')
def index():
    print("post slash")
    pass

#== tester =========================================================================================
# Original test version.  Manual tests successfully passsed
#===================================================================================================
# @bt_app.get('/')
# def index(foo=None):
#     if 'counter' in session.data:
#         session.data['counter'] += 1
#     else:
#         session.data['counter'] = 0
#
#     return '''
#         <pre>
#             Session sid: %s
#             Session user: %s
#             Session data: %s
#             "?foo=...": %s
#         </pre>
#     ''' % (session.sid, session.user, session.data, foo)
#
#
# bt_app.run()


serve(bt_app)
