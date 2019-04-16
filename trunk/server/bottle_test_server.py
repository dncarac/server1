from bottle import route, run
from requests import get
from threading import Thread
from time import sleep
import cfg

path = "/"
srv = "http://%s:%s%s" % (cfg.SERVER_NAME, cfg.SERVER_PORT, path)
pg = '''<!DOCTYPE HTML>
<html>
<head>
<title>Title of the document</title>
</head>

<body>
The content of the document......
</body>

</html>
'''

params = {'typed':"typed line", 'assigned':"assigned"}


@route(path)
def hello():
    return pg

#===============================================================================
#
#===============================================================================


def tester():
    r = get(srv)
    assert r.text == pg
    print("test complete")
    return


tthread = Thread(target=tester, name="test thread")
tthread.start()
run(host=cfg.SERVER_NAME, port=cfg.SERVER_PORT, debug=True)
tthread.join()
