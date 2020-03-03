#! /usr/bin/python3
# -*- coding: utf-8 -*-
''' Server

@summary: Server for TypeLines!

@detailed_description: Receives requests from client, extracts data, retrieves requested
data, returns data to client in response.

__CreatedOn__ = "2019-11-05"
__UpdatedOn__ = "2020-03-02"

@author: Den
@copyright: Copyright © 2019-2020 Den
@license: ALL RIGHTS RESERVED
'''

''' Error Handling
Suggested error handling in Bottle documentation --
https://bottlepy.org/docs/dev/api.html#bottle.Bottle.error

def error_handler_500(error):
    return 'error_handler_500'

app.error(code=500, callback=error_handler_500)

@app.error(404)
def error_handler_404(error):
    return 'error_handler_404'
'''

import bottle as bt; bt_app = bt.Bottle()    # @UnresolvedImport
from waitress import serve    # @UnresolvedImport
import canister    # @UnresolvedImport
from canister import session    # @UnresolvedImport
import cfg
import TaskData as TD
from dataclasses import *
# import sys

bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())

# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# _LOG.level = logging.INFO
# _LOG.level = logging.DEBUG
_LOG.level = logging.TRACE


# logging.disable(logging.WARN)
# Disable logging at or below this level (WARN default)
def trace_only(record):
    return record.levelno == logging.TRACE

# _LOG.addFilter(trace_only)


# region - Module constants
#   upload
FILE_KEY = 'upfile'
TASKDATA_KEY = "Task-Data"

#   download
DEFAULT_PAGE = "Default page"
# endregion


# region - ERROR HANDLERS =====================================================
@bt_app.error(400)    # Bad request
def error_handler_400(error_code):
    return "Error 400\n %s" % error_code


@bt_app.error(404)    # Not found
def error_handler_404(error_code):
    return "Error 404\n %s" % error_code


@bt_app.error(405)    # Not found
def error_handler_405(error_code):
    return "Error 405\n %s" % error_code


@bt_app.error(500)    # Server error
def error_handler_500(error_code):
    return "Error 500\n %s" % error_code


@bt_app.error(501)    # Not implemented
def error_handler_501(error_code):
    return "Error 501\n %s" % error_code

# endregion ===================================================================


# region - Server functions ===================================================
def ReceiveFile():
    ''' ReceiveFile --
    @summary:
        Receive task file from client
        Create TaskData instance from file
        Store TaskData instance in session data

    @precondition: request.files data contains - {'TaskData': {"upfile": <bytes>}, ...}

    @postcondition: response header which contains - {"Ack" : "Ack" | "Nack", ...}

    @return: True if no errors; None if error occurred.
    @rtype: bool | None
    '''

    _LOG.trace("Enter ReceiveFile")
#------------------------------------------------------------------------------
    # Check if file exists in upload
    try:
        tskfil = bt.request.files[FILE_KEY].file.read()
    except bt.BottleException as e:
        _LOG.exception("No task file found in request.\n  %s" % e)
        _LOG.trace("Leave ReceiveFile returning HTTP response code 404.")
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        return bt.HTTPError(404, "Not Found - Unable to retrieve the task file from client request.\n%s" % e)
    _LOG.debug("tskfil: %s" % tskfil)

    # Check if file represents a valid task file which produces valid task data
    tf = TD.TaskFile()
    _LOG.debug("tf:\n%s\n%s" % (type(tf), tf))
    td = tf.read(tskfil)
    _LOG.debug("td:\n%s\n%s" % (type(td), td))
    if tf is None or td is None:
        _LOG.debug("Unable to create TaskData from uploaded taskfile")
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.trace("Leave ReceiveFile returning HTTP response code 406")
        return bt.HTTPError(406, "Not Acceptable - Unable to create TaskData from uploaded taskfile")
    _LOG.debug("taskdata:\n%s" % td)

    # Assign task data to session data and return Ack
    session.data[TASKDATA_KEY] = td
    _LOG.info("session data:\n%s\n%s" % (type(session.data[TASKDATA_KEY]), session.data[TASKDATA_KEY]))
    bt.response.set_header(cfg.RTN_KEY, cfg.ACK)
    _LOG.info("returned response header: %s" % bt.response.headers[cfg.RTN_KEY])
#------------------------------------------------------------------------------
    _LOG.trace("Leave ReceiveFile")
    return "200 Success - Task file received successfully"


def SendClientConfig():
#     ''' SendClientConfig --
#
#     '''
    _LOG.trace("Enter Server.SendClientConfig")
#------------------------------------------------------------------------------
    _LOG.debug("SendClientConfig session data:\n%s" % session.data)
    ccd = TD.TaskData(session.data).get_client_config_data()
    _LOG.debug("ccd: %s" % ccd)
    bt.response.set_header(cfg.RTN_KEY, ccd)
    _LOG.info("returned response header: %s" % bt.response.headers[cfg.RTN_KEY])
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendClientConfig")
    return "200 Success - Client configuration returned successfully"


def SendTypingData():
#     ''' SendTypingData --
#
#     '''

    _LOG.trace("  Enter Server.SendTypingData")
#------------------------------------------------------------------------------
    td = session.data[TASKDATA_KEY]
    _LOG.debug("Session data:\n%s" % td)
    typed_line = bt.request.forms.get(cfg.TYPINGDATA_KEY, None)
    _LOG.debug("typed_line: %s" % typed_line)
#     td = TD.TaskData(session.data)
    _LOG.debug("td:\n%s" % td)
    typing_data = td.next_typing_data(typed_line)
    _LOG.debug("typing data: ", typing_data)
    _LOG.debug("typing data: %s" % typing_data)
    bt.response.set_header(cfg.RTN_KEY, typing_data)
    _LOG.info("returned response header: %s" % bt.response.headers[cfg.RTN_KEY])
#------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendTypingData")
    return "200 Success - Typing data returned successfully"


def SendDistractionData():
#     ''' SendDistractionData --
#
#     '''
    _LOG.trace("  Enter Server.SendDistractionData")
# #------------------------------------------------------------------------------
#     bt.response.set_header(cfg.TL_HDR + 'Distraction-Data', (5.5, 'Title1', 'Msg1'))
# #------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendDistractionData")


def SendSummary():
#     ''' SendSummary --
#
#     '''
    _LOG.trace("  Enter Server.SendSummary")
# #------------------------------------------------------------------------------

# #------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendSummary")


def Cancel():
#     '''  Cancel--
#
#     '''
    _LOG.trace("  Enter Server.Cancel")
# #------------------------------------------------------------------------------
    pass
# #------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.Cancel")

# endregion ===================================================================


test_select = {
    "SendFile": ReceiveFile,
    "GetClientConfig": SendClientConfig,
    "GetTypingData": SendTypingData,
    "GetDistractionData": SendDistractionData,
    "GetSummary": SendSummary,
    "Cancel": Cancel,
    }


@bt_app.get("/")
def server_get():
    '''
    Get request
    '''
    return DEFAULT_PAGE


@bt_app.post("/")
def server_post():
    ''' server_post --
    @summary: Receives post requests to path "/", extracts forms data, returns requested data (if
    any)

    @cvar bt.request.forms: (dict) Contains http request data

    @cvar bt.response.headers: (dict) Contains http response data

    @precondition: bt.request.forms (dict) contains data representing the html request from the client.

    @postcondition: bt.response.headers contains data to be returned to the client
    '''
    _LOG.trace("Enter Server.server_post")
#------------------------------------------------------------------------------
    # Check if Msg-Type exists
    msg_type = bt.request.forms.get(cfg.MSG_TYPE_KEY, None)
    _LOG.debug("msg_type: %s" % msg_type)
    if msg_type is None:
        _LOG.debug("400 - Bad Request - The request did not include a 'Msg-Type' header.")
        return bt.HTTPError(400, "Bad Request - The request did not include a 'Msg-Type' header.")

    # Check if Msg-Type header points to an existing function
    test_func = test_select.get(msg_type, None)
    _LOG.debug("test_func: %s" % test_func)
    if test_func is None:
        _LOG.debug("501 - Not Implemented - The requested function is not implemented.")
        return bt.HTTPError(501, "Not Implemented - The requested function is not implemented.")
    _LOG.debug("test_func name: %s()" % test_func.__name__)

    # Execute function
    rtn = test_func()
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.server_post returning %s" % rtn)
    return rtn


if __name__ == '__main__':
    serve(bt_app)

# Quick Tests --
#     import requests as rq
#     from threading import Thread
#     url = cfg.SERVER
#
#     print("\nStart")
#
#     # Start server ============================================================
#     def start_server():
#         _LOG.trace("Start backup_server_folder")
#         serve(bt_app)
#         _LOG.trace("Server closed")
#
#     server_thread = Thread(None, start_server)
#     server_thread.start()
#
#     # region - GET ============================================================
#     sys.stderr.write("\n")
#     _LOG.info("get(url)")
#     r = rq.get(url)
#     assert str(r) == "<Response [200]>"
#     assert r.status_code == 200
#     assert r.text == "Server_get page"
#     # endregion ===============================================================
#
#     # region - POST, SendFile, FOWtaskfile ====================================
#     sys.stderr.write("\n")
#     _LOG.info("post(url, SendFile, FOWtaskfile)")
#     files = {FILE_KEY: open(cfg.TASK_PATH + "breast task 5.tsk", 'rb')}
#     data = {cfg.MSG_TYPE_KEY: "SendFile"}
#     r = rq.post(url, data=data, files=files)
#     assert str(r) == "<Response [200]>"
#     assert r.status_code == 200
#     assert r.text == "Server_post return"
#     assert r.headers[cfg.ACK] == cfg.ACK
#     # endregion ===============================================================
#
#     #region -  POST, SendFile, TLtaskfile =====================================
#     sys.stderr.write("\n")
#     _LOG.info("post(url, SendFile, TLtaskfile)")
#     files = {FILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb')}
#     data = {cfg.MSG_TYPE_KEY: "SendFile"}
#     r = rq.post(url, data=data, files=files)
#     assert str(r) == "<Response [200]>"
#     assert r.status_code == 200
#     assert r.text == "Server_post return"
#     assert r.headers[cfg.ACK] == cfg.ACK
#     # endregion ===============================================================
#
#     #region -  POST, GetClientConfig ==========================================
#     sys.stderr.write("\n")
#     _LOG.info("post(url, GetClientConfig)")
#     data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}
#     r = rq.post(url, data=data)
#     assert str(r) == "<Response [200]>"
#     assert r.status_code == 200
#     assert r.text == "Server_post return"
#     assert r.headers[cfg.CLIENT_CONFIG_KEY] == {'hidden' : 'False'}
#     # endregion ===============================================================
#
#     print("\nDone")
