#! ../venv/scripts python
# -*- coding: utf-8 -*-
''' bottle_test_server -

@summary: Prelim bottle test_server and tester

@description: Implement a bottle test_server, then test the request/responses of that test_server.

__CreatedOn__="2019-06-16"
__UpdatedOn__="2019-11-12"

@version: 0.1
@author: Den
@copyright: Copyright © 2019 Den
@license: ALL RIGHTS RESERVED
'''
# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger("bottle_test_server -- ")
# _LOG.level = logging.INFO
# _LOG.level = logging.TRACE
# endregion

import bottle as bt
import cfg

# region - web page setup
path = "/"
srv = "http://%s:%s%s" % (cfg.SERVER_NAME, cfg.SERVER_PORT, path)
srv = "http://localhost"
print(srv)
static_path = 'static'
static_page = "index.htm"
previous_typed = "previously typed line"
title = "new title"
msg = "new message"
assigned = "new assigned line"
up_params = {'X-typed': previous_typed}
down_params = {
                'X-title': title,
                'X-msg': msg,
                'X-assigned': assigned,
               }
# endregion


@bt.route(path)
def hello():

    _LOG.trace("Enter @gget_allhello")
#------------------------------------------------------------------------------
    typed = bt.request.headers['X-typed']
    print("X-typed:", typed)
    for k, v in {**up_params, **down_params}.items():
        bt.response.set_header(k, v)
    with open("./static/index.htm") as f:
        bt.response.body = f.read()
#------------------------------------------------------------------------------
    _LOG.trace("Leave @gget_allhello")
    return bt.response


pass
#===============================================================================
# Web site above
#-------------------------------------------------------------------------------
# Test below
#===============================================================================

if __name__ == '__main__':
    import requests as rq
    from threading import Thread

    def tester():
        url = cfg.SERVER
        print("url: " + url)
        r = rq.get(url=cfg.SERVER, headers=up_params)
        print(r)
        assert str(r) == "<Response [200]>"
#         print(r.text)
        assert r.text == '''<html>
    <head>
        <title>Python is awesome!</title>
    </head>
    <body>
        <h1>Typelines</h1>
        <p>Congratulations! The HTTP Server is working!</p>
    </body>
</html>'''
#         print("\nHeaders --")
#         print(r.headers)
#         for h in r.headers:
#             print("    %s: %s" % (h, r.headers[h]))
        hdrs = r.headers
        del hdrs['Date']
        assert hdrs == {'Server': 'WSGIServer/0.2 CPython/3.7.3', 'X-Typed': 'previously typed line', 'X-Title': 'new title', 'X-Msg': 'new message', 'X-Assigned': 'new assigned line', 'Content-Type': 'text/html; charset=UTF-8'}
        print("\n*** test complete ***")
        return

    tthread = Thread(target=tester, name="test thread")
    tthread.start()
    bt.run(host=cfg.SERVER_NAME, port=cfg.SERVER_PORT, debug=True)
    tthread.join()
