#! /usr/bin/python3
# -*- coding: utf-8 -*-
''' test_server.py --

First test module

Testing module for setting up Client-backup_server_folder communications

__CreatedOn__="2018-04-02"
__UpdatedOn__="2020-03-02"

@author: Den
@copyright: Copyright © 2018-2020 Den
@license: ALL RIGHTS RESERVED
'''
import requests as rq    # @UnresolvedImport
import cfg
import sys
import pytest
# from TLexceptions import *

# region - logging setup
import logging
logging.basicConfig()
_LOG = logging.getLogger(__name__)
logging.basicConfig(
    datefmt='%m/%d/%Y %I:%M:%S %p',
    format='%(asctime)s %(message)s',
    )


# _LOG.level = logging.TRACE
# _LOG.level = logging.DEBUG
# _LOG.level = logging.INFO
def trace_only(record):
    return record.levelno == logging.TRACE


_LOG.addFilter(trace_only)
# endregion

url = "http://localhost:8080/"

# region - Module constants
#   upload
FILE_KEY = 'upfile'
#   download
DEFAULT_PAGE = "Default page"
# endregion


# @pytest.mark.skip("Successfully completed")
def test_get():
    ''' test_get --
    '''
    _LOG.trace("Enter test_get")
#--------------------------------------------------------------------------------
    r = rq.get(url)
    assert str(r) == "<Response [200]>"
    assert r.status_code == 200
    assert r.text == DEFAULT_PAGE
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_get")


# @pytest.mark.skip("Successfully completed")
def test_header_no_msg_type():
    ''' test_header_no_msg_type --
    '''
    _LOG.trace("Enter test_header_no_msg_type")
#--------------------------------------------------------------------------------
    r = rq.post(url)
    assert str(r) == '<Response [400]>'
    assert r.status_code == 400
    assert r.text == '''Error 400\n (400, "Bad Request - The request did not include a 'Msg-Type' header.")'''
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_header_no_msg_type")


# @pytest.mark.skip("Successfully completed")
def test_msg_type_bad_function():
    ''' test_msg_type_bad_function --
    '''
    _LOG.trace("Enter test_msg_type_bad_function")
#--------------------------------------------------------------------------------
    hdrs = {cfg.MSG_TYPE_KEY: "dummy"}
    r = rq.post(url, data=hdrs)
    assert str(r) == '<Response [501]>'
    assert r.status_code == 501
    assert r.text == "Error 501\n (501, 'Not Implemented - The requested function is not implemented.')"
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_msg_type_bad_function")


# @pytest.mark.skip("Successfully completed")
def test_SendFile_function_FOW():
    ''' test_SendFile_function_FOW --
    '''
    _LOG.trace("Enter test_SendFile_function_FOW")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {FILE_KEY: open(cfg.TASK_PATH + "breast task 5.tsk", 'rb')}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        r = s.post(url, data=data, files=files)
        assert str(r) == "<Response [200]>"
        assert r.status_code == 200
        assert r.text == "200 Success - Task file received successfully"
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_FOW")


# @pytest.mark.skip("Successfully completed")
def test_SendFile_function_TL():
    ''' test_SendFile_function --
    '''
    _LOG.trace("Enter test_SendFile_function_TL")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {FILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb')}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        r = s.post(url, data=data, files=files)
        assert str(r) == "<Response [200]>"
        assert r.status_code == 200
        assert r.text == "200 Success - Task file received successfully"
        assert r.headers[cfg.RTN_KEY] == cfg.ACK
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_TL")


# @pytest.mark.skip("Successfully completed")
def test_ClientConfig_function():
    ''' test_ClientConfig_function --
    '''
    _LOG.trace("Enter test_ClientConfig_function")
#--------------------------------------------------------------------------------------------------
    s = rq.Session()
    files = {FILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb')}

    data = {cfg.MSG_TYPE_KEY: "SendFile"}
    r = s.post(url, data=data, files=files)
    assert str(r) == "<Response [200]>"
    assert r.status_code == 200
    assert r.text == "200 Success - Task file received successfully"
    assert r.headers[cfg.RTN_KEY] == cfg.ACK

    data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}
    r = s.post(url, data=data)
    assert str(r) == "<Response [200]>"
    assert r.status_code == 200
    assert r.text == "200 Success - Client configuration returned successfully"
    assert r.headers[cfg.RTN_KEY] == "{'hidden': False}"
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_ClientConfig_function")


# @pytest.mark.skip("Successfully completed")
def test_TypingData_function():
    ''' test_TypingData_function
    '''
    _LOG.trace("Enter test_TypingData_function")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {FILE_KEY: open(cfg.TASK_PATH + "../tasks/test typing data task.tsk", 'rb')}

        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        r = s.post(url, data=data, files=files)
        assert str(r) == "<Response [200]>"
        assert r.status_code == 200
        assert r.text == "200 Success - Task file received successfully"
        assert r.headers[cfg.RTN_KEY] == cfg.ACK

        data = {cfg.MSG_TYPE_KEY: "GetTypingData",
                cfg.TYPEDLINE_KEY: None}
        r = s.post(url, data=data)
        assert str(r) == "<Response [200]>"
        assert r.status_code == 200
        assert r.text == "200 Success - Typing data returned successfully"
        assert r.headers[cfg.RTN_KEY] == "{'title': 'Typing Dialog Title', 'line': 'Line 1', 'msg': 'Msg'}"
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_TypingData_function")


if __name__ == "__main__":
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

    rtn = pytest.main(["-vvs", __file__])
    print("Pytest returned:\n  %s - %s" % (rtn, exit_code[rtn]))
