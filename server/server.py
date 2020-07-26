# !./venv/bin
# -*- coding: utf-8 -*-
''' Server

@summary: Server for TypeLines!

@detailed_description: Receives requests from client, extracts data, retrieves requested
data, returns data to client in response.

__CreatedOn__ = "2019-11-05"
__UpdatedOn__ = "2020-07-22"

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

# region - Module Constants
# STATIC_PATH = "./static"
# FOW_PATH = "./FOW/fow.htm"
# TL_PATH = "./TL/index.html"


# region - Imports
import bottle as bt; bt_app = bt.Bottle()    # @UnresolvedImport
from waitress import serve    # @UnresolvedImport
import canister    # @UnresolvedImport
from canister import session    # @UnresolvedImport
import cfg
import TaskData as TD
import time
# endregion

bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())


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
    _LOG.trace("Enter Server.ReceiveFile")
#------------------------------------------------------------------------------
    # Check if file exists in upload
    try:
        tskfil = bt.request.files[cfg.TASKFILE_KEY].file.read()
    except bt.BottleException as e:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.exception("No task file found in request.\n  %s" % e)
        _LOG.error("No task file found in request.")
        _LOG.trace("Leave ReceiveFile returning HTTP status code: ", cfg.NOT_FOUND_ERROR_T)
        return
    _LOG.debug("tskfil: %s" % tskfil)

    # Check if tskfil represents a valid task file
    td = TD.TaskFile().read(tskfil)
    _LOG.debug("td: %s" % td)
    if td is None:
        bt.response.status = cfg.INVALID_DATA
        _LOG.error("Unable to create TaskData from uploaded taskfile")
        _LOG.trace("Leave ReceiveFile returning HTTP status code %s" % cfg.INVALID_DATA_T)
        return

    # Assign task data to session data
    session.data[cfg.SESSION_TASKDATA_KEY] = td
    _LOG.debug("Session data:\n%s" % session.data[cfg.SESSION_TASKDATA_KEY])
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
        ccd = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    except (bt.BottleException, TypeError, ValueError) as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Error retrieving session data in Server.SendClientConfig\n  %s" % e)
        _LOG.error("Error retrieving session data in Server.SendClientConfig")
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.SERVER_ERROR_T)
        return
    _LOG.debug("ccd: %s\n%s" % (type(ccd), ccd))

    if ccd is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.error("No ClientConfigData in session data for Server.SendClientConfig.")
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.NOT_FOUND_ERROR_T)
        return

    ccd = ccd.get_client_config_data()
    _LOG.info("ccd: %s %s" % (type(ccd), ccd))
    if ccd is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.error("ClientConfigData not in session data for Server.SendClientConfig.")
        _LOG.trace("Leave Server.SendClientConfig returning HTTP status code: %s" % cfg.NOT_FOUND_ERROR_T)
        return

    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendClientConfig returning: %s" % bt.response.status)
    return


def SendTypingData():
    ''' SendTypingData --
    '''

    _LOG.trace("Enter Server.SendTypingData")
#------------------------------------------------------------------------------
    try:
        td = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    except (bt.BottleException, TypeError, ValueError) as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Error retrieving session data in Server.SendTypingData\n  %s" % e)
        _LOG.error("Error retrieving session data in Server.SendTypingData")
        _LOG.trace("Leave Server.SendTypingData returning HTTP status code: %s" % cfg.SERVER_ERROR_T)
        return
    _LOG.debug("session data taskdata: %s" % td)

    if td is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.error("Session data does not exist in Server.SendTypingData.")
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.NOT_FOUND_ERROR_T)
        return

    try:
        typed_line = bt.request.forms.get(cfg.TYPEDLINE_KEY, None)
    except (bt.BottleException, ValueError, TypeError) as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Error retrieving typed line from request.forms.\n  %s" % e)
        _LOG.error("Error retrieving typed line from request.forms.")
        _LOG.trace("Leave SendTypingData returning %s" % cfg.SERVER_ERROR_T)
        return
    _LOG.debug("typed_line: %s" % typed_line)

    if typed_line is None:
        bt.response.status = cfg.CLIENT_ERROR
        _LOG.error("Typed line not in request.headers in Server.SendTypingData.")
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.CLIENT_ERROR_T)
        return

    typing_data = td.next_typing_data(typed_line)    # Dictionary of values, or END_TASK or Error (None)
    _LOG.debug("typing_data: %s" % typing_data)
    if typing_data is None:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.error("No typing data from taskdata object.")
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.SERVER_ERROR_T)
        return

    try:
        bt.response.set_header(cfg.RTN_KEY, typing_data)
    except bt.BottleException as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Unable to return typing_data to the client correctly./n  ", e)
        _LOG.error("Unable to return typing_data to the client correctly.")
        _LOG.trace("Leave Server.SendTypingData returning %s" % cfg.SERVER_ERROR_T)
        return

    rtn = bt.response.headers[cfg.RTN_KEY]
    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendTypingData returning: %s\n%s" % (cfg.SUCCESS_T, rtn))
    return


def SendDistractionData():
    ''' SendDistractionData --
    '''
    _LOG.trace("Enter Server.SendDistractionData")
#------------------------------------------------------------------------------
    try:
        td = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    except bt.BottleError as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Cannot retrieve taskdata from session data in Server.SendDistractionData\n  %s: e")
        _LOG.error("Cannot retrieve taskdata from session data in Server.SendDistractionData")
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.SERVER_ERROR_T)
        return
    _LOG.debug("td: %s" % td)

    if td is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.error("No taskdata in session data in Server.SendDistractionData.")
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.NOT_FOUND_ERROR_T)
        return

    distraction_data = td.next_distraction_data()    # Dictionary of values, or Error (None)
    _LOG.debug("distraction_data: %s" % distraction_data)
    if distraction_data is None:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.error("Distraction data was not returned correctly from taskdata.next_distraction_data.")
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.SERVER_ERROR_T)
        return

    try:
        bt.response.set_header(cfg.RTN_KEY, distraction_data)
    except bt.BottleException as e:
        bt.response.status = cfg.SERVER_ERROR
        _LOG.exception("Unable to place distraction_data in response.header in Server.SendDistractionData./n  ", e)
        _LOG.error("Unable to place distraction_data in response.header in Server.SendDistractionData")
        _LOG.trace("Leave Server.SendDistractionData returning %s" % cfg.SERVER_ERROR_T)
        return
    _LOG.debug("bt.response.headers[cfg.RTN_KEY]: %s" % bt.response.headers[cfg.RTN_KEY])

    bt.response.status = cfg.SUCCESS
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendDistractionData returning %s\n  %s" % (cfg.SUCCESS_T, bt.response.headers[cfg.RTN_KEY]))
    return


def SendSummary():
    ''' SendSummary --
    '''
    _LOG.trace("  Enter Server.SendSummary")
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.SendSummary")


def Cancel():
#     '''  Cancel--
#
#     '''
    _LOG.trace("  Enter Server.Cancel")
# #------------------------------------------------------------------------------
    try:
        del session
    except bt.BottleException as e:
        _LOG.exception("Error terminating a session.\n  %s" % e)
# #------------------------------------------------------------------------------
    _LOG.trace("  Leave Server.Cancel")

# region - Dispatcher =============================================================================


svr_func_select = {
    "SendFile": ReceiveFile,
    "GetClientConfig": SendClientConfig,
    "GetTypingData": SendTypingData,
    "GetDistractionData": SendDistractionData,
    "GetSummary": SendSummary,
    "Cancel": Cancel,
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
    _LOG.trace("Enter Server.server_post")
#---------------------------------------------------------------------------------------------------
    # Check if Msg-Type header exists
    msg_type = bt.request.forms.get(cfg.MSG_TYPE_KEY, None)
    _LOG.debug("msg_type: %s" % msg_type)
    if msg_type is None:
        bt.response.status = cfg.CLIENT_ERROR
        _LOG.error("There is no 'Msg-Type' header.")
        _LOG.trace("Leave Server.server_post returning: %s" % (cfg.CLIENT_ERROR_T))
        return

    # Check if Msg-Type header points to an existing function
    svr_func = svr_func_select.get(msg_type, None)
    _LOG.debug("svr_func: %s" % svr_func)
    if svr_func is None:
        bt.response.status = cfg.NOT_IMPLEMENTED_ERROR
        _LOG.error("The requested function is not implemented.")
        _LOG.trace("Leave Server.server_post returning %s" % cfg.NOT_IMPLEMENTED_ERROR_T)
        return

    _LOG.debug("svr_func name: %s()" % svr_func.__name__)

    # Execute function
    svr_func()
#------------------------------------------------------------------------------
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
