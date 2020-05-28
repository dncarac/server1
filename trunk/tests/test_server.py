#! /usr/bin/python3
# -*- coding: utf-8 -*-
''' test_server.py --

First test module

Testing module for setting up Client-backup_server_folder communications

__CreatedOn__="2018-04-02"
__UpdatedOn__="2020-05-27"

@author: Den
@copyright: Copyright © 2018-2020 Den
@license: ALL RIGHTS RESERVED
'''
import requests as rq    # @UnresolvedImport
import cfg
import pytest
import sys
# from TLexceptions import *

# region - logging setup
import logging
# def trace_only(record):
#     return record.levelno == logging.TRACE
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# _LOG.addFilter(trace_only)
_LOG.level = logging.TRACE
# _LOG.level = logging.DEBUG
# _LOG.level = logging.INFO
# endregion

url = cfg.SERVER


@pytest.mark.skip("Successfully completed")
def test_get():
    ''' test_get --
    Test get command.
    Should produce HTML page.
    '''
    _LOG.trace("Enter test_get")
#--------------------------------------------------------------------------------
    r = rq.get(url)

    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.status_code: %s" % r.status_code)
    assert r.text == cfg.DEFAULT_PAGE
    assert r.status_code == cfg.SUCCESS
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_get")


@pytest.mark.skip("Successfully completed")
def test_header_no_msg_type():
    ''' test_header_no_msg_type --
    '''
    _LOG.trace("Enter test_header_no_msg_type")
#--------------------------------------------------------------------------------
    r = rq.post(url)

    _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
    assert r.status_code == cfg.CLIENT_ERROR
    assert r.text == ""
    assert r.headers[cfg.RTN_KEY] == cfg.NACK
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_header_no_msg_type")


@pytest.mark.skip("Successfully completed")
def test_msg_type_bad_function():
    ''' test_msg_type_bad_function --
    '''
    _LOG.trace("Enter test_msg_type_bad_function")
#--------------------------------------------------------------------------------
    hdrs = {cfg.MSG_TYPE_KEY: "dummy"}

    r = rq.post(url, data=hdrs)

    _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
    assert r.status_code == cfg.NOT_IMPLEMENTED_ERROR
    assert r.text == ""
    assert r.headers[cfg.RTN_KEY] == cfg.NACK
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_msg_type_bad_function")


@pytest.mark.skip("Successfully completed")
def test_SendFile_function_FOW():
    ''' test_SendFile_function_FOW --
    '''
    _LOG.trace("Enter test_SendFile_function_FOW")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tsk", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(url, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_FOW")


@pytest.mark.skip("Successfully completed")
def test_SendFile_function_TL():
    ''' test_SendFile_function --
    '''
    _LOG.trace("Enter test_SendFile_function_TL")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(url, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_TL")


@pytest.mark.skip("Successfully completed")
def test_ClientConfig_no_session_data():
    ''' test_ClientConfig_no_session_data --
    '''
    sys.stderr.write("\n\n")
    _LOG.trace("Enter test_ClientConfig_no_session_data")
#-- Get client config-------------------------------------------------------------------------------------------
    data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

    r = rq.post(url, data=data)

    _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers.get(cfg.RTN_KEY, None))
    assert r.status_code == cfg.NOT_FOUND_ERROR
    assert r.text == ""
    assert r.headers[cfg.RTN_KEY] == cfg.NACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_ClientConfig_no_session_data\n\n")


# @pytest.mark.skip("Successfully completed")
def test_ClientConfig_no_client_config_data():
    ''' test_ClientConfig_no_client_config_data --
    '''

    sys.stderr.write("\n\n")
    _LOG.trace("Enter test_ClientConfig_no_client_config_data")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
    #-- Receive file------------------------------------------------------------------------------------------------
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "no_config_data.tlt", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(url, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
    #-- Get client config-------------------------------------------------------------------------------------------
        data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

        r = s.post(url, data=data)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers.get(cfg.RTN_KEY, None))
        assert r.status_code == cfg.NOT_FOUND_ERROR
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.NACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_ClientConfig_no_client_config_data\n\n")


@pytest.mark.skip("Successfully completed")
def test_ClientConfig_function():
    ''' test_ClientConfig_function --
    '''
    sys.stderr.write("\n\n")
    _LOG.trace("Enter test_ClientConfig_function")
#-- Send file -----------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(url, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#------ Get client config-------------------------------------------------------------------------------------------
        data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

        r = s.post(url, data=data)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == "{'hidden': False, 'rand_win_loc': False, 'lrg_button': True, 'rand_button_loc': False}"
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_no_client_config_data\n\n")


@pytest.mark.skip("Successfully completed")
def test_TypingData_function():
    ''' test_TypingData_functionv
    '''
    sys.stderr.write("\n\n")
    _LOG.trace("Enter test_TypingData_function")
#------ Send file -----------------------------------------------------------------------------------------------
    with rq.Session() as s:
        _LOG.info("\n\nSend file")
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "test typing data task.tsk", 'rb').read()}
        _LOG.debug("files sent: %s" % files)
        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        _LOG.debug("data sent: %s" % data)

        r = s.post(url, data=data, files=files)

        _LOG.debug("r.status_code (post): %s" % r.status_code)
        _LOG.debug("r.text (post): %s" % r.text)
        _LOG.debug("r.headers (post): %s" % r.headers)
        _LOG.debug("r.headers[cfg.RTN_KEY] (post): %s" % r.headers[cfg.RTN_KEY])
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#------ Send first line-------------------------------------------------------------------------------------------
        _LOG.info("\n\nSend first line (cfg.START_TASK)")
        send_list = [cfg.START_TASK, "Line 1", "Line 2"]
        expected_list = ["{'title': 'Typing Dialog Title', 'line': 'Line 1', 'msg': 'Msg'}",
                         "{'title': 'Typing Dialog Title', 'line': 'Line 2', 'msg': 'Msg'}",
                         cfg.END_TASK
                        ]
        for sent, expected in zip(send_list, expected_list):
            _LOG.debug("sent to server: %s ... expected from server: %s}'" % (sent, expected))
            data = {cfg.MSG_TYPE_KEY: "GetTypingData",
                    cfg.TYPEDLINE_KEY: sent}
            _LOG.debug("data: %s" % data)

            r = s.post(url, data=data)

            _LOG.debug("r.status_code: %s" % r.status_code)
            _LOG.debug("r.text: %s" % r.text)
            _LOG.debug("r.headers: %s" % r.headers)
            _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers[cfg.RTN_KEY])
            assert r.status_code == cfg.SUCCESS
            assert r.text == ""
            assert r.headers[cfg.RTN_KEY] == expected

#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_TypingData_function\n\n")
#
#
# def test_DistractionData_function():
#     ''' test_DistractionData_function
#     '''
#     _LOG.trace("Enter test_DistractionData_function")
# #--------------------------------------------------------------------------------------------------
#     with rq.Session() as s:
#         files = {FILE_KEY: open(cfg.TASK_PATH + "../tasks/test distraction data task.tsk", 'rb')}
#
#         data = {cfg.MSG_TYPE_KEY: "SendFile"}
#         r = s.post(url, data=data, files=files)
#         assert str(r) == "<Response [200]>"
#         assert r.status_code == 200
#         assert r.text == "200 Success - Task file received successfully"
#         assert r.headers[cfg.RTN_KEY] == cfg.ACK
#
#         data = {cfg.MSG_TYPE_KEY: "GetDistractionData",
#                 cfg.TYPEDLINE_KEY: None}
#         r = s.post(url, data=data)
#         assert str(r) == "<Response [200]>"
#         assert r.status_code == 200
#         assert r.text == "200 Success - Distraction data returned successfully"
#         assert r.headers[cfg.RTN_KEY] == "{'title': 'Distraction Dialog Title', 'msg': 'Msg'}"
# #--------------------------------------------------------------------------------------------------
#     _LOG.trace("Leave test_DistractionData_function")


if __name__ == "__main__":
    import TaskData as TD
    td = TD.TaskData()
    print(td)
    td.config_data = None
    print(td)
    tf = TD.TaskFile()
    print(tf)
    res = tf.write(td, cfg.TASK_PATH + "no_config_data.tlt")
    print("res: %s\n" % res)
    print(tf)
    td = TD.TaskFile().read(cfg.TASK_PATH + "no_config_data.tlt")
    print(td)
    exit()

    ''' (from pytest docs):
    Running pytest can result in six different exit codes:
        Exit code 0:    All tests were collected and passed successfully
        Exit code 1:    Tests were collected and run but some of the tests failed
        Exit code 2:    Test execution was interrupted by the user
        Exit code 3:    Internal error happened while executing tests
        Exit code 4:    pytest command line usage error
        Exit code 5:    No tests were collected
    '''

    exit_code = {
        0: "All tests were collected and passed successfully",
        1: "Tests were collected and run but some of the tests failed",
        2: "Test execution was interrupted by the user",
        3: "Internal error happened while executing tests",
        4: "pytest command line usage error",
        5: "No tests were collected",
        }

    rtn = pytest.main(["-vvs", __file__])    # @UndefinedVariable
    print("Pytest returned:\n  %s - %s" % (rtn, exit_code[rtn]))
