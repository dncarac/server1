#! /usr/bin/python3
# -*- conding: utf-8 -*-
# ''' Server
#
# @summary: Server for TypeLines!
#
# @detailed_description: Receives requests from client, extracts data, retrieves requested
# data, returns data to client in response.
#
# __CreatedOn__ = "2019-11-05"
# __UpdatedOn__ = "2020-02-06"
#
# @author: Den
# @copyright: Copyright © 2019-2020 Den
# @license: ALL RIGHTS RESERVED
# '''
#
# ''' Error Handling
# Suggested error handling in Bottle documentation --
# https://bottlepy.org/docs/dev/api.html#bottle.Bottle.error
#
# def error_handler_500(error):
#     return 'error_handler_500'
#
# app.error(code=500, callback=error_handler_500)
#
# @app.error(404)
# def error_handler_404(error):
#     return 'error_handler_404'
# '''

import bottle as bt; bt_app = bt.Bottle()    # @UnresolvedImport
from waitress import serve    # @UnresolvedImport
import canister    # @UnresolvedImport
from canister import session    # @UnresolvedImport
import cfg
import TaskData as TD
# from TLexceptions import TL_InvalidFile
# from io import BytesIO
# import sys

bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())

# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# _LOG.level = logging.INFO
_LOG.level = logging.DEBUG
# _LOG.level = logging.TRACE
# logging.disable(logging.WARN)
# Disable logging at or below this level (WARN default)
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


@bt_app.error(500)
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

    @precondition: request data contains - tskfil: {"tskfil": <bytes>, ...}

    @postcondition: response header which contains - ack: {"ack", <str of bool>}
                True if tskfil received successfully, False otherwise
    '''
    _LOG.trace("Enter ReceiveFile")
#------------------------------------------------------------------------------
    _LOG.debug("    Start received files --")
    _LOG.debug("      Files --")
    for k, v in bt.request.files.items():
        print("        %s -> %s" % (k, v))
    tskfil = bt.request.forms.get(cfg.TASKFILE_KEY, None)
    _LOG.debug("      tskfil: %s" % tskfil)
    if tskfil is None:
        bt.response.set_header('Ack', 'False')
        _LOG.debug("      Missing task file")
        _LOG.trace("      Leave ReceiveFile returning header Ack: False")
        return bt.HTTPError(400, "Bad Request - No 'Task-File' key")
    tf = TD.TaskFile()
    td = tf.read(tskfil.encode())
    _LOG.debug("      td ---: %s" % td)
    if td is None:
        bt.response.set_header('Ack', 'False')
        _LOG.debug("      Missing taskdata")
        _LOG.trace("      Leave ReceiveFile returning header Ack: False")
        return bt.HTTPError(404, "Not Found - File content is not a valid task file.")
    session.data[cfg.TASKDATA_KEY] = td
    bt.response.set_header('Ack', 'True')
    _LOG.info("session.data['Task-Data']:\n%s" % session.data[cfg.TASKDATA_KEY])
    _LOG.debug("    End received files --")
#------------------------------------------------------------------------------
    _LOG.trace("Leave ReceiveFile returning response header Ack: True")


def SendClientConfig():
#     ''' SendClientConfig --
#
#     '''
    _LOG.trace("  Enter Server.SendClientConfig")
#------------------------------------------------------------------------------
    bt.response.set_header('Config-Data')
#------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendClientConfig")


def SendTypingData():
#     ''' SendTypingData --
#
#     '''
    _LOG.trace("  Enter Server.SendTypingData")
# #------------------------------------------------------------------------------
#     typed_ln = bt.request.get_header(cfg.TL_HDR + 'Typed-Line')
#     _LOG.info("     Typed-Line: " + str(typed_ln))
#     if typed_ln == 'None':
#         bt.response.set_header(cfg.TL_HDR + 'Typing-Data', ("Title1", "Line1", "Msg1"))
#     if typed_ln == "Typed1":
#         bt.response.set_header(cfg.TL_HDR + 'Typing-Data', ("Title2", "Line2", "Msg2"))
#     if typed_ln == "Typed2":
#         bt.response.set_header(cfg.TL_HDR + 'Typing-Data', None)
# #------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendTypingData")


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
    "SendClientConfig": SendClientConfig,
    "SendTypingData": SendTypingData,
    "SendDistractionData": SendDistractionData,
    "SendSummary": SendSummary,
    "Cancel": Cancel,
    }


@bt_app.get("/")
def server_get():
    '''
    Get request
    '''
#     return bt.HTTPError(405, "Get request has no content")
    return "Server_get page"


@bt_app.post("/")
def server_post():
    ''' backup_server_folder --
    @summary: Receives post requests to path "/", extracts forms data, returns requested data (if
    any)

    @cvar bt.request,forms: (dict) Contains http request data

    @cvar bt.response.headers: (dict) Contains http response data

    @precondition: bt.request.forms (dict) contains data representing the html request from the client.

    @postcondition: bt.response.headers contains data to be returned to the client
    '''
    _LOG.trace("Enter Server.backup_server_folder")
#--------------------------------------------------------------------------------------------------
    # Log data values
    _LOG.debug("  Start backup_server_folder --")

    tskfil = bt.request.files.upfile.file.read()
    print("tskfil: %s" % tskfil)
    tf = TD.TaskFile()
    td = tf.read(tskfil)
    session.data['tdata'] = td
    print("session data:\n%s" % session.data['tdata'])
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave Server.backup_server_folder")
    return "Server_post return"    # Return text with pre-set headers


if __name__ == '__main__':

    import requests as rq
    from threading import Thread
    url = cfg.SERVER

    print("\nStart")

    def start_server():
        _LOG.trace("Start backup_server_folder")
        serve(bt_app)
        _LOG.trace("Server closed")

    server_thread = Thread(None, start_server)
    server_thread.start()

    # POST, sendfile, TLtaskfile ==============================================
    _LOG.info("\npost(url, SendFile, TLtaskfile)")

    data = {cfg.MSG_TYPE_KEY: "SendFile"}
    with open(cfg.TASK_PATH + 'breast task 5.tsk', 'rb') as f:
        r = rq.post('http://Dell:8080', data=data, files={'upfile': f})

    print("\nDone")
