#! /usr/bin/python3
# -*- coding: utf-8 -*-
''' Server

@summary: Server for TypeLines!

@detailed_description: Receives requests from client, extracts data, retrieves requested
data, returns data to client in response.

__CreatedOn__ = "2019-11-05"
__UpdatedOn__ = "2020-05-26"

@author: Den
@copyright: Copyright © 2019-2020 Den
@license: ALL RIGHTS RESERVED
'''

# region - Imports
import bottle as bt; bt_app = bt.Bottle()    # @UnresolvedImport
from waitress import serve    # @UnresolvedImport
import canister    # @UnresolvedImport
from canister import session    # @UnresolvedImport
import cfg
import TaskData as TD
from dataclasses import *    # @UnusedWildImport
import sys
# endregion

bt_app.config.load_config('./conf/canister.cfg')
bt_app.install(canister.Canister())

# region - logging setup
import logging
logging.basicConfig()
# logging.disable(logging.WARN)
_LOG = logging.getLogger(__name__)
# _LOG.level = logging.INFO
# _LOG.level = logging.DEBUG
_LOG.level = logging.TRACE


# Disable logging at or below this level (WARN default)
def trace_only(record): return record.levelno == logging.TRACE

# _LOG.addFilter(trace_only)

# endregion
#


def ReceiveFile():
    ''' Server.ReceiveFile --
    @summary:
        Receive task file from client
        Create TaskData instance from file
        Store TaskData instance in session data

    @precondition: request.files data contains - {'Task-File': <bytes>, 'Msg-Type': "ReceiveFile"}

    @postcondition: response status code which contains - 200 / Ack; or
                    response status code which contains - 404 | 406 / Nack.

    @return: status code 200 / Ack; or
             status code 404 | 406 / Nack.
        @rtype: status code / str
    '''
    _LOG.trace("Enter Server.ReceiveFile")
#------------------------------------------------------------------------------
    # Check if file exists in upload
    try:
        tskfil = bt.request.files[cfg.TASKFILE_KEY].file.read()
    except bt.BottleException as e:
        bt.response.status = cfg.NOT_FOUND_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.exception("No task file found in request.\n  %s" % e)
        _LOG.error(cfg.NOT_FOUND_ERROR_T, "No task file found in request.")
        _LOG.trace("Leave ReceiveFile returning Nack / HTTP status code", cfg.NOT_FOUND_ERROR_T)
        return
    _LOG.debug("tskfil: %s" % tskfil)

    # Check if tskfil represents a valid task file
    td = TD.TaskFile().read(tskfil)
    if td is None:
        bt.response.status = cfg.INVALID_DATA
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.INVALID_DATA_T, "Unable to create TaskData from uploaded taskfile")
        _LOG.trace("Leave ReceiveFile returning Nack / HTTP status code.", cfg.INVALID_DATA)
        return
    _LOG.debug("td:\n%s" % td)

    # Assign task data to session data and return Ack
    session.data[cfg.SESSION_TASKDATA_KEY] = td
    bt.response.status = cfg.SUCCESS
    bt.response.set_header(cfg.RTN_KEY, cfg.ACK)
    _LOG.info("Session data:\n%s" % session.data[cfg.SESSION_TASKDATA_KEY])
    _LOG.info("Returned status: %s" % bt.response.status)
    _LOG.info("Return %s" % cfg.ACK)
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.ReceiveFile returning %s / HTTP response code %s." % (cfg.ACK, cfg.SUCCESS))
    return


def SendClientConfig():
    ''' SendClientConfig --
    '''
    _LOG.trace("Enter Server.SendClientConfig")
#------------------------------------------------------------------------------
    td = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    if td is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.NOT_FOUND_ERROR_T, "Session data unavailable for Server.SendClientConfig.")
        _LOG.trace("Leave Server.SendClientConfig returning Nack / HTTP status code", cfg.NOT_FOUND_ERROR)
        return
    _LOG.debug("td:\n%s" % td)

    ccd = td.get_client_config_data()
    if ccd is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        _LOG.error(cfg.NOT_FOUND_ERROR_T, "Client config data not retrieved for Server.SendClientConfig.")
        _LOG.trace("Leave Server.SendClientConfig returning Nack / HTTP status code.", cfg.NOT_FOUND_ERROR)
        return
    _LOG.debug("ccd: %s" % ccd)

    bt.response.set_header(cfg.RTN_KEY, ccd)
    bt.response.status = cfg.SUCCESS
    _LOG.info("Returned status: %s" % bt.response.status)
    _LOG.info("Returned response header: %s" % bt.response.headers[cfg.RTN_KEY])
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendClientConfig returning: %s\n%s" % (bt.response.status, bt.response.headers[cfg.RTN_KEY]))
    return


def SendTypingData():
    ''' SendTypingData --
    '''
    _LOG.trace("Enter Server.SendTypingData")
#------------------------------------------------------------------------------
    td = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    if td is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.NOT_FOUND_ERROR_T, "Session data not retrieved correctly in Server.SendTypingData.")
        _LOG.trace("Leave Server.SendTypingData returning Nack / %s" % cfg.NOT_FOUND_ERROR)
        return
    _LOG.debug("td: %s" % td)

    typed_line = bt.request.forms.get(cfg.TYPEDLINE_KEY, None)
    if typed_line is None:
        bt.response.status = cfg.CLIENT_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.CLIENT_ERROR_T, "Typed line not retrieved correctly from form upload.")
        _LOG.trace("Leave Server.SendTypingData returning Nack / %s" % cfg.CLIENT_ERROR)
        return
    _LOG.debug("typed_line: %s" % typed_line)

    typing_data = td.next_typing_data(typed_line)    # Dictionary of values, or END_TASK or Error (None)
    if typing_data is None:
        bt.response.status = cfg.SERVER_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.SERVER_ERROR_T, "Typing data was not extracted correctly.")
        _LOG.trace("Leave Server.SendTypingData returning Nact / %s" % cfg.SERVER_ERROR)
        return
    _LOG.debug("typing_data: %s" % typing_data)

    try:
        bt.response.set_header(cfg.RTN_KEY, typing_data)
    except bt.BottleException as e:
        bt.response.status = cfg.SERVER_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.exception(cfg.SERVER_ERROR_T, "Unable to return typing_data to the client correctly./n  ", e)
        _LOG.trace("Leave Server.SendTypingData returning Nack / %s" % cfg.SERVER_ERROR)
        return None
    rtn = bt.response.headers[cfg.RTN_KEY]
    bt.response.status = cfg.SUCCESS
    bt.response.set_header(cfg.RTN_KEY, cfg.ACK)
    _LOG.info("Returned status code: %s" % bt.response.status)
    _LOG.info("Returned response header: %s" % rtn)
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendTypingData returning Ack / %s" % cfg.SUCCESS)
    return


def SendDistractionData():
    ''' SendDistractionData --
    '''
    _LOG.trace("Enter Server.SendDistractionData")
#------------------------------------------------------------------------------
    td = session.data.get(cfg.SESSION_TASKDATA_KEY, None)
    if td is None:
        bt.response.status = cfg.NOT_FOUND_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.NOT_FOUND_ERROR_T, "Session data not retrieved correctly in Server.SendDistractionData.")
        _LOG.trace("Leave Server.SendDistractionData returning Nack / %s" % cfg.NOT_FOUND_ERROR)
        return
    _LOG.debug("td: %s" % td)

    distraction_data = td.next_distraction_data()    # Dictionary of values, or Error (None)
    if distraction_data is None:
        bt.response.status = cfg.SERVER_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.error(cfg.SERVER_ERROR_T, "Distraction data was not extracted correctly.")
        _LOG.trace("Leave Server.SendDistractionData returning Nack / %s" % cfg.SERVER_ERROR)
        return
    _LOG.debug("distraction_data: %s" % distraction_data)

    try:
        bt.response.set_header(cfg.RTN_KEY, distraction_data)
    except bt.BottleException as e:
        bt.response.status = cfg.SERVER_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.exception(cfg.SERVER_ERROR_T, "Unable to return distraction_data to the client correctly./n  ", e)
        _LOG.trace("Leave Server.SendDistractionData returning Nack / %s" % cfg.SERVER_ERROR)
        return None
    rtn = bt.response.headers[cfg.RTN_KEY]
    bt.response.status = cfg.SUCCESS
    bt.response.set_header(cfg.RTN_KEY, cfg.ACK)
    _LOG.info("Returned status code: %s" % bt.response.status)
    _LOG.info("Returned response header: %s" % rtn)
#------------------------------------------------------------------------------
    _LOG.trace("Leave Server.SendTypingData returning Ack / %s" % cfg.SUCCESS)
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
    pass
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


@bt_app.get("/")
def server_get():
    '''
    Get request
    '''
    return cfg.DEFAULT_PAGE


@bt_app.post("/")
def server_post():
    ''' Server.server_post --
    @summary: Receives post requests to path "/", extracts forms data, returns requested data (if
    any).

    @precondition: bt.request.forms (dict) contains data representing the html request from the
    client.

    @postcondition: bt.response.headers contains data to be returned to the client (if any).
    '''

    sys.stderr.write("\n\n")
    _LOG.trace("Enter Server.server_post")
#------------------------------------------------------------------------------
    # Check if Msg-Type header exists
    msg_type = bt.request.forms.get(cfg.MSG_TYPE_KEY)
    _LOG.debug("msg_type: %s" % msg_type)

    # Check if Msg-Type exists
    if msg_type is None:
        bt.response.status = cfg.CLIENT_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.debug("%s - Bad Request - The request did not include a 'Msg-Type' header." % cfg.CLIENT_ERROR)
        _LOG.trace("Leave Server.server_post returning status code: %s %s" % (cfg.CLIENT_ERROR, cfg.NACK))
        return

    # Check if Msg-Type header points to an existing function
    svr_func = svr_func_select.get(msg_type, None)
    _LOG.debug("svr_func: %s" % svr_func)

    if svr_func is None:
        bt.response.status = cfg.NOT_IMPLEMENTED_ERROR
        bt.response.set_header(cfg.RTN_KEY, cfg.NACK)
        _LOG.debug("%s - Not Implemented - The requested function is not implemented." % cfg.NOT_IMPLEMENTED_ERROR)
        _LOG.trace("Leave Server.server_post returning %s" % cfg.NOT_IMPLEMENTED_ERROR)
        return
    _LOG.debug("svr_func name: %s()" % svr_func.__name__)

    # Execute function
    svr_func()
#------------------------------------------------------------------------------
    sys.stderr.write("\n\n")
    return


if __name__ == '__main__':
    serve(bt_app)
