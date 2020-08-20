# !./venv/bin
# -*- coding: utf-8 -*-
''' Server

@summary: Server for TypeLines!

@detailed_description: Receives requests from client, extracts data, retrieves requested
data, returns data to client in response.

__CreatedOn__ = "2019-11-05"
__UpdatedOn__ = "2020-08-19"

@author: Den
@copyright: Copyright © 2019-2020 Den
@license: ALL RIGHTS RESERVED
'''
# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# logging.disable(logging.WARN)
# _LOG.level = logging.INFO
# _LOG.level = logging.DEBUG
# _LOG.level = logging.TRACE

# Disable logging at or below this level (WARN default)


def trace_only(record): return record.levelno == logging.TRACE

# _LOG.addFilter(trace_only)

# endregion


import time
import bottle as bt; bt_app = bt.Bottle()    # @UnresolvedImport
from waitress import serve    # @UnresolvedImport
import canister    # @UnresolvedImport
from canister import session    # @UnresolvedImport
import cfg
import TaskData as TD
# from Log import Log    # ; TlLog = Log()    # TlLog ID is made global

bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())

# Module variables
_running = False
_assigned_line = cfg.START_TASK


def ReceiveFile():
    ''' Server.ReceiveFile --
    @summary:
        Receive task file from client
        Create TaskData instance from file
        Store TaskData instance in session data

    @precondition: request.files data contains - {'Task-File': <bytes>, 'Msg-Type': "ReceiveFile"}

    @postcondition: response status code which contains - 200; or
                    response status code which contains - 404 | 406.

    @return: status code 200; or
             status code 404 | 406.
        @rtype: status code
    '''
    _LOG.trace("\n\n======  ReceiveFile  ===================================")
    _LOG.trace("Enter Server.ReceiveFile")
#------------------------------------------------------------------------------
    # Check if file exists in upload
    try:
        tskfil = bt.request.files[cfg.REQ_TASKFILE].file.read()
    except (bt.BottleException, IOError, TypeError, ValueError) as e:
        bt.response.status = cfg.ERR_NOT_FOUND_ERROR
        _LOG.exception("No task file found in request.\n  %s" % e)
        _LOG.trace("Leave ReceiveFile returning HTTP status code: ", cfg.ERR_NOT_FOUND_ERROR_T)
        Cancel("No task file found in request.")
        return
    _LOG.debug("tskfil: %s" % tskfil)

    # Check if tskfil represents a valid task file
    td = TD.TaskFile().read(tskfil)
    _LOG.debug("td: %s" % td)
    if td is None:
        bt.response.status = cfg.ERR_INVALID_DATA
        _LOG.trace("Leave ReceiveFile returning HTTP status code %s" % cfg.ERR_INVALID_DATA_T)
        Cancel("Unable to create TaskData from uploaded taskfile")
        return

    # Assign task data to session data
    session.data[cfg.SESSION_TASKDATA] = td
    _LOG.debug("Task data in session data:\n%s" % session.data[cfg.SESSION_TASKDATA])

    # Start log with task data and assign to session data
    # TlLog.open(td)    # Open TL log
    # session.data[cfg.SESSION_LOG] = TlLog
    # _LOG.debug("Log in session data:\n%s" % session.data[cfg.SESSION_LOG])

    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.ReceiveFile returning HTTP status code %s." % cfg.SUCCESS_T)
    return


def SendClientConfig():
    ''' Server.SendClientConfig --
    '''

    _LOG.trace("Enter Server.SendClientConfig")
#---------------------------------------------------------------------------------------------------
    try:
        td = session.data.get(cfg.SESSION_TASKDATA, None)
#         TlLog = session.data.get(cfg.SESSION_LOG, None)
    except (bt.BottleException, TypeError, ValueError) as e:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.exception("Error retrieving session data in Server.SendClientConfig\n  %s" % e)
        Cancel("Error retrieving session data in Server.SendClientConfig")
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.ERR_SERVER_ERROR_T)
        return
    _LOG.debug("td:\n%s" % td)
#     _LOG.debug("TlLog:\n%s" % TlLog)

    if td is None:
        bt.response.status = cfg.ERR_NOT_FOUND_ERROR
        Cancel("No ClientConfigData found in session data for Server.SendClientConfig.")
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.ERR_NOT_FOUND_ERROR_T)
        return

#     if TlLog is None:
#         bt.response.status = cfg.ERR_NOT_FOUND_ERROR
#         _LOG.error("No TlLog found in session data for Server.SendClientConfig.")
#         _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.ERR_NOT_FOUND_ERROR_T)
#         return

    ccd = td.get_client_config_data()
    _LOG.info("ccd:\n  %s" % ccd)

    if ccd is None:
        bt.response.status = cfg.ERR_NOT_FOUND_ERROR
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.ERR_NOT_FOUND_ERROR_T)
        Cancel("ClientConfigData not in session data for Server.SendClientConfig.")
        return

#     TlLog.add(cfg.LOG_CLIENT_CONFIG_DATA, ccd)
    bt.response.headers[cfg.RES_RTN] = ccd
    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendClientConfig returning: %s:\n  %s" % (cfg.SUCCESS_T, ccd))
    return


def SendTypingData():
    ''' SendTypingData --
    '''
    global _running, _assigned_line
    _LOG.trace("\n\n======  SendTypingData  ===================================")
    _LOG.trace("Enter Server.SendTypingData")
# region - Receive typed line from the client.---------------------------------------------------------------
    try:    # Session data
        td = session.data.get(cfg.SESSION_TASKDATA, None)
#         TlLog = session.data.get(cfg.SESSION_LOG, None)
    except (bt.BottleException, TypeError, ValueError) as e:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.exception("Error retrieving session data in Server.SendTypingData\n  %s" % e)
        _LOG.trace("Leave Server.SendTypingData returning HTTP status code: %s" % cfg.ERR_SERVER_ERROR_T)
        Cancel("Error retrieving session data in Server.SendTypingData")
        return
    _LOG.debug("session data taskdata: %s" % td)

    if td is None:
        bt.response.status = cfg.ERR_NOT_FOUND_ERROR
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.ERR_NOT_FOUND_ERROR_T)
        Cancel("TaskData Session data does not exist in Server.SendTypingData.")
        return

#     if TlLog is None:
#         bt.response.status = cfg.ERR_NOT_FOUND_ERROR
#         _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.ERR_NOT_FOUND_ERROR_T)
#         Cancel("TlLog Session data does not exist in Server.SendTypingData.")
#         return

    try:    # Typed ine
        typed_line = bt.request.forms.get(cfg.REQ_TYPED_LINE, None)
    except (bt.BottleException, ValueError, TypeError) as e:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.exception("Error retrieving typed line from request.forms.\n  %s" % e)
        _LOG.trace("Leave SendTypingData returning %s" % cfg.ERR_SERVER_ERROR_T)
        Cancel("Error retrieving typed line from request.forms.\n  %s" % e)
        return
    _LOG.debug("typed_line: %s" % typed_line)

    if typed_line is None:
        bt.response.status = cfg.ERR_CLIENT_ERROR
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.ERR_CLIENT_ERROR_T)
        Cancel("Typed line not in request.headers in Server.SendTypingData.")
        return
#     TlLog.add("TYPED_LINE", typed_line)
# endregion

# region - Retrieve typing data from TaskData ---------------------------------------------------------------
# TODO Correct logic for last return (END_TASK)
    if not _running and typed_line == cfg.START_TASK:    # First time through
        _LOG.info("First!")
        _running = True
        _match = True
        t_data = td.typing_data.next()    # triple or None

    elif _running and isinstance(typed_line, str):    # Middle times through - i.e. a line has been typed
        _match = typed_line == _assigned_line.reversed if td.typing_data.reversed else _assigned_line

        if td.completion_data.is_done(_match):    # Last time through
            _LOG.info("Done!")
            _LOG.trace("Leave TaskData.next_typing_data returning END_TASK")
            t_data = cfg.END_TASK    # str
        else:
            _LOG.info("Next!")
            t_data = td.typing_data.next()    # {'title': title, 'line': line, 'msg': msg}

    else:    # Error - Neither a string nor START_TASK received from typing dialog.
        _LOG.trace("Leave TaskData.next_typing_data returning None")
        Cancel("Neither a string nor START_TASK received from the typing dialog.")
        return
# endregion

# region - Process typing data (t_data)
    _LOG.debug("t_data: %s %s" % (type(t_data), t_data))
    # TlLog.add("TYPING_DATA", t_data)
    if isinstance(t_data, dict):    # dict
        _assigned_line = t_data['line']    # line
        _LOG.info("assigned line: %s %s" % (type(_assigned_line), _assigned_line))
        bt.response.set_header(cfg.RES_RTN, t_data)
        bt.response.status = cfg.SUCCESS
    elif t_data == cfg.END_TASK:    # END_TASK
        _running = False
        bt.response.set_header(cfg.RES_RTN, t_data)
        bt.response.status = cfg.SUCCESS
    else:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.trace("Leave server..SendTypingData returning %s" % cfg.ERR_SERVER_ERROR_T)
        Cancel("Typing data is None, or not a dictionary or END_TASK")
        return
# endregion
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendTypingData returning: %s\n  %s" % (cfg.SUCCESS_T, t_data))
    return


def SendDistractionData():
    ''' SendDistractionData --
    '''
    _LOG.trace("Enter Server.SendDistractionData")
#------------------------------------------------------------------------------
    try:
        td = session.data.get(cfg.SESSION_TASKDATA, None)
#         TlLog = session.data.get(cfg.SESSION_LOG, None)
    except bt.BottleError as e:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.exception("Cannot retrieve session data in Server.SendDistractionData\n  %s:" % e)
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.ERR_SERVER_ERROR_T)
        Cancel("Cannot retrieve session data in Server.SendDistractionData")
        return
    _LOG.debug("td: %s" % td)
#     _LOG.debug("TlLog: %s" % TlLog)

    if td is None:
        bt.response.status = cfg.ERR_NOT_FOUND_ERROR
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.ERR_NOT_FOUND_ERROR_T)
        Cancel("No taskdata in session data in Server.SendDistractionData.")
        return

#     if TlLog is None:
#         bt.response.status = cfg.ERR_NOT_FOUND_ERROR
#         _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.ERR_NOT_FOUND_ERROR_T)
#         Cancel("TlLog not found in session data in Server.SendDistractionData.")
#         return

    distraction_data = td.next_distraction_data()    # Dictionary of values, or Error (None)
    _LOG.debug("distraction_data: %s" % distraction_data)
    if distraction_data is None:
        bt.response.status = cfg.ERR_SERVER_ERROR
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.ERR_SERVER_ERROR_T)
        Cancel("Distraction data not found in session data.")
        return

#     TlLog.add(cfg.LOG_DISTRACTION_DATA, distraction_data)
    bt.response.set_header(cfg.RES_RTN, distraction_data)
    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendDistractionData returning %s\n  %s" % (cfg.SUCCESS_T, bt.response.headers[cfg.RES_RTN]))
    return


def SendSummary():
    ''' SendSummary --
    '''
    _LOG.trace("  Enter Server.SendSummary")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendSummary")


def Cancel(msg):
#     '''  Cancel--
#
#     '''
    _LOG.trace("Enter Server.Cancel with %s" % msg)
# #------------------------------------------------------------------------------
    # TlLog.add("CANCEL", msg)
    # _LOG.info("\nCancel: %s\n------------------\n\n" % msg)
    print("\nCancel: %s\n------------------\n\n" % msg)

#     try:
#         del session
#     except bt.BottleException as e:
#         _LOG.exception("Error terminating a session.\n  %s" % e)
# #------------------------------------------------------------------------------
    _LOG.trace("Leave Server.Cancel")


# region - Dispatcher =============================================================================
svr_func_select = {
    cfg.REQ_TASKFILE: ReceiveFile,
    cfg.REQ_CLIENT_CONFIG_DATA: SendClientConfig,
    cfg.REQ_TYPED_LINE: SendTypingData,
    cfg.REQ_DISTRACTION_DATA: SendDistractionData,
    cfg.REQ_SUMMARY: SendSummary,
    cfg.CANCEL: Cancel,
    }
# endregion =======================================================================================


@bt_app.post("/")
def server_post():
    ''' Server.server_post --
    @summary: Receives post requests to path "/", extracts forms data, returns requested data (if
    any).

    @precondition: bt.request.forms (dict) contains data representing the html request from the
    client.

    @postcondition: bt.response.headers contains data to be returned to the client (if any).
    '''
    _LOG.trace("\n\n==  SERVER  ===================================")
    _LOG.trace("Enter server.server_post")
#---------------------------------------------------------------------------------------------------
    # Check if Msg-Type header exists
    msg_type = bt.request.forms.get(cfg.REQ_MSG_TYPE, None)
    _LOG.debug("msg_type: %s" % msg_type)
    if msg_type is None:
        bt.response.status = cfg.ERR_CLIENT_ERROR
        _LOG.trace("Leave Server.server_post returning: %s" % (cfg.ERR_CLIENT_ERROR_T))
        Cancel("There is no 'Msg-Type' header in the request.")
        return

    # Check if Msg-Type header points to an existing function
    svr_func = svr_func_select.get(msg_type, None)
    _LOG.debug("svr_func: %s" % svr_func)
    if svr_func is None:
        bt.response.status = cfg.ERR_NOT_IMPLEMENTED_ERROR
        _LOG.trace("Leave Server.server_post returning %s" % cfg.ERR_NOT_IMPLEMENTED_ERROR_T)
        Cancel("The requested function is not implemented in server.")
        return
    _LOG.debug("svr_func name: %s()" % svr_func.__name__)

    # Execute function
    svr_func()
#---------------------------------------------------------------------------------------------------
    return


@bt_app.post("/time")
def time_post():
    ''' Server.time_post --
    @summary: Receives post requests to path "/time", returns time as time.time float.
    '''
    _LOG.trace("Enter Server.time_post")
#---------------------------------------------------------------------------------------------------
    rtn = time.time()
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.time_post returning: %s" % rtn)
    return str(rtn)


if __name__ == '__main__':
    serve(bt_app, port=cfg.SERVER_PORT)
