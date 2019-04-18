# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger("bottle_test_server -- ")
# _LOG.level = logging.INFO
# _LOG.level = logging.TRACE
# endregion

import bottle as bt
import requests as rq
from threading import Thread
import cfg

# region - web page setup
path = "/"
srv = "http://%s:%s%s" % (cfg.SERVER_NAME, cfg.SERVER_PORT, path)
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

    _LOG.trace("Enter @get hello")
#------------------------------------------------------------------------------
    typed = bt.request.headers.get('X-typed')
    for k, v in {**up_params, **down_params}.items():
        bt.response.set_header(k, v)
#     bt.response.body = "hello"
#------------------------------------------------------------------------------
    _LOG.trace("Leave @get hello")
    with open("./static/index.htm") as f:
        bt.response.body = f.read()
    return bt.response


pass
#===============================================================================
# Web site above
#-------------------------------------------------------------------------------
# Test below
#===============================================================================

if __name__ == '__main__':

    def tester():

        r = rq.get(srv, headers=up_params)
        print(r)
        assert str(r) == "<Response [200]>"
        print(r.text)
        assert r.text == '''<html>
    <head>
        <title>Python is awesome!</title>
    </head>
    <body>
        <h1>Typelines</h1>
        <p>Congratulations! The HTTP Server is working!</p>
    </body>
</html>'''
        print("\nHeaders --")
        for h in r.headers:
            print("    %s: %s" % (h, r.headers[h]))
        print("\n*** test complete ***")
        return

    tthread = Thread(target=tester, name="test thread")
    tthread.start()
    bt.run(host=cfg.SERVER_NAME, port=cfg.SERVER_PORT, debug=True)
    tthread.join()
