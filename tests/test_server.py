#! /usr/bin/python3
# -*- coding: utf-8 -*-
''' test_server.py --

First test module

Testing module for setting up Client-backup_server_folder communications

__CreatedOn__="2018-04-02"
__UpdatedOn__="2020-06-30"

@author: Den
@copyright: Copyright © 2018-2020 Den
@license: ALL RIGHTS RESERVED
'''
import requests as rq    # @UnresolvedImport
import cfg
import pytest
# import sys
# from TLexceptions import *

# region - logging setup
import logging
# def trace_only(record):
#     return record.levelno == logging.TRACE
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# _LOG.addFilter(trace_only)
# _LOG.level = logging.TRACE
# _LOG.level = logging.DEBUG
# _LOG.level = logging.INFO
# endregion


# @pytest.mark.skip("Successfully completed")
def test_header_no_msg_type():
    ''' test_header_no_msg_type --
    '''
    _LOG.trace("Enter test_header_no_msg_type")
#--------------------------------------------------------------------------------
    r = rq.post(cfg.SERVER)

#     _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    assert r.status_code == cfg.CLIENT_ERROR
    assert r.text == ""
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_header_no_msg_type")


# @pytest.mark.skip("Successfully completed")
def test_msg_type_bad_function():
    ''' test_msg_type_bad_function --
    '''
    _LOG.trace("Enter test_msg_type_bad_function")
#--------------------------------------------------------------------------------
    hdrs = {cfg.MSG_TYPE_KEY: "dummy"}

    r = rq.post(cfg.SERVER, data=hdrs)

    _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    assert r.status_code == cfg.NOT_IMPLEMENTED_ERROR
    assert r.text == ""
#--------------------------------------------------------------------------------
    _LOG.trace("Leave test_msg_type_bad_function")


# @pytest.mark.skip("Successfully completed")
def test_SendFile_function_FOW():
    ''' test_SendFile_function_FOW --
    '''
    _LOG.trace("Enter test_SendFile_function_FOW")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tsk", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(cfg.SERVER, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_FOW")


# @pytest.mark.skip("Successfully completed")
def test_SendFile_function_TL():
    ''' test_SendFile_function --
    '''
    _LOG.trace("Enter test_SendFile_function_TL")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(cfg.SERVER, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_SendFile_function_TL")


# @pytest.mark.skip("Successfully completed")
def test_ClientConfig_no_session_data():
    ''' test_ClientConfig_no_session_data --
    '''
    _LOG.trace("Enter test_ClientConfig_no_session_data")
#-- Get client config-------------------------------------------------------------------------------------------
    data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

    r = rq.post(cfg.SERVER, data=data)

    _LOG.debug("r.status_code: %s" % r.status_code)
    _LOG.debug("r.text: %s" % r.text)
    _LOG.debug("r.headers: %s" % r.headers)
    _LOG.debug("r.headers[cfg.RTN_KEY]: %s" % r.headers.get(cfg.RTN_KEY, None))
    assert r.status_code == cfg.NOT_FOUND_ERROR
    assert r.text == ""
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_ClientConfig_no_session_data\n\n")


# @pytest.mark.skip("Successfully completed")
def test_ClientConfig_no_client_config_data():
    ''' test_ClientConfig_no_client_config_data --
    '''
    _LOG.trace("Enter test_ClientConfig_no_client_config_data")
#--------------------------------------------------------------------------------------------------
    import TaskData as TD
    with rq.Session() as s:
    #-- Receive file------------------------------------------------------------------------------------------------
        fn = cfg.TASK_PATH + "no_config_data.tlt"
        files = {cfg.TASKFILE_KEY: open(fn, 'rb').read()}
        td = TD.TaskFile().read(cfg.TASK_PATH + 'no_config_data.tlt')
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(cfg.SERVER, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
    #-- Get client config-------------------------------------------------------------------------------------------
        data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

        r = s.post(cfg.SERVER, data=data)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.NOT_FOUND_ERROR
        assert r.text == ""
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_ClientConfig_no_client_config_data\n\n")


# @pytest.mark.skip("Successfully completed")
def test_ClientConfig_function():
    ''' Server.test_ClientConfig_function --
    '''
    _LOG.trace("Enter Server.test_ClientConfig_function")
#  -------------------------------------------------------------------------------------------------
    with rq.Session() as s:
#------ Send file -----------------------------------------------------------------------------------------------
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "breast task 5.tlt", 'rb').read()}
        data = {cfg.MSG_TYPE_KEY: "SendFile"}

        r = s.post(cfg.SERVER, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""

#------ Get client config-------------------------------------------------------------------------------------------
        data = {cfg.MSG_TYPE_KEY: "GetClientConfig"}

        r = s.post(cfg.SERVER, data=data)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave Server.test_ClientConfig_function\n\n")


# @pytest.mark.skip("Successfully completed")
def test_TypingData_function():
    ''' test_TypingData_functionv
    '''
    _LOG.trace("Enter test_TypingData_function")
#------ Send file -----------------------------------------------------------------------------------------------
    with rq.Session() as s:
        _LOG.info("\n\nSend file")
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "test typing data task.tsk", 'rb').read()}
        _LOG.debug("files sent: %s" % files)
        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        _LOG.debug("data sent: %s" % data)

        r = s.post(cfg.SERVER, data=data, files=files)

        _LOG.debug("r.status_code: %s" % r.status_code)
        _LOG.debug("r.text: %s" % r.text)
        _LOG.debug("r.headers: %s" % r.headers)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""
#------ Send lines----------------------------------------------------------------------------------
        _LOG.info("\n\nSend lines")
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

            r = s.post(cfg.SERVER, data=data)

            _LOG.debug("r.status_code: %s" % r.status_code)
            _LOG.debug("r.text: %s" % r.text)
            _LOG.debug("r.headers: %s" % r.headers)
            assert r.status_code == cfg.SUCCESS
            assert r.text == ""
            assert r.headers[cfg.RTN_KEY] == expected
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_TypingData_function\n\n")


# @pytest.mark.skip("Successfully completed")
def test_DistractionData_function():
    ''' test_DistractionData_function
    '''
    import sys
    _LOG.trace("Enter test_DistractionData_function")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "../tasks/test distraction data task.tsk", 'rb')}

        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        r = s.post(cfg.SERVER, data=data, files=files)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""

        data = {cfg.MSG_TYPE_KEY: "GetDistractionData",
                cfg.TYPEDLINE_KEY: None}
        r = s.post(cfg.SERVER, data=data)
        assert r.status_code == 200
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == "{'d_title': 'Distraction Title', 'd_msg': 'Message 1'}"

        r = s.post(cfg.SERVER, data=data)
        assert r.status_code == 200
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == "{'d_title': 'Distraction Title', 'd_msg': 'Message 2'}"

        r = s.post(cfg.SERVER, data=data)
        assert r.status_code == 200
        assert r.text == ""
        assert r.headers[cfg.RTN_KEY] == "{'d_title': 'Distraction Title', 'd_msg': 'Message 1'}"
#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_DistractionData_function")


@pytest.mark.skip("To be developed")
def test_terminate_session_function():
    ''' test_DistractionData_function
    '''
    _LOG.trace("Enter test_DistractionData_function")
#--------------------------------------------------------------------------------------------------
    with rq.Session() as s:
        files = {cfg.TASKFILE_KEY: open(cfg.TASK_PATH + "../tasks/test distraction data task.tsk", 'rb')}

        data = {cfg.MSG_TYPE_KEY: "SendFile"}
        r = s.post(cfg.SERVER, data=data, files=files)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""

        data = {cfg.MSG_TYPE_KEY: "Cancel"}
        r = s.post(cfg.SERVER, data=data)
        print("session s: %s" % s)
        print("r.status_code: %s" % r.status_code)
        print("r.text: %s" % r.text)
        assert r.status_code == cfg.SUCCESS
        assert r.text == ""

#--------------------------------------------------------------------------------------------------
    _LOG.trace("Leave test_DistractionData_function")


if __name__ == "__main__":
# Setup to try to test for no client_config_data
#     import TaskData as TD
#     td = TD.TaskData()
#     print(td)
#     td.config_data = None
#     print(td)
#     tf = TD.TaskFile()
#     print(tf)
#     res = tf.write(td, cfg.TASK_PATH + "no_config_data.tlt")
#     print("res: %s\n" % res)
#     print(tf)
#     td = TD.TaskFile().read(cfg.TASK_PATH + "no_config_data.tlt")
#     print(td)
#     exit()

# Setup to create "breast task 5.tlt"
#     import TaskData as TD
#     tf = TD.TaskFile()
#     print("tf: %s" % tf)
#     td = tf.read(cfg.TASK_PATH + "breast task 5.tsk")
#     print("td: %s" % td)
#     print("tf: %s" % tf)
#     tf.write(td, cfg.TASK_PATH + "breast task 5.tlt")
#     print("tf: %s" % tf)
#     exit()

# Setup to create "test distraction data task.tsk"
#     from TaskData import TaskData, TaskFile
#     td = TaskData()
#     print("td: %s" % td)
#     print("td.distraction_data: %s" % td.distraction_data)
#     print("td.distraction_data.d_titles: %s" % td.distraction_data.d_titles)
#
#     print("td.distraction_data.d_titles.lst: %s" % td.distraction_data.d_titles.lst)
#     td.distraction_data.d_titles.lst = ['Distraction Title']
#     print("td.distraction_data.d_titles.lst: %s" % td.distraction_data.d_titles.lst)
#
#     print("td.distraction_data.d_msgs.lst: %s" % td.distraction_data.d_msgs.lst)
#     td.distraction_data.d_msgs.lst = ['Message 1', 'Message 2']
#     print("td.distraction_data.d_msgs.lst: %s" % td.distraction_data.d_msgs.lst)
#
#     tf = TaskFile()
#     print("tf: %s" % tf)
#     tf.write(td, cfg.TASK_PATH + "test distraction data task.tsk")
#     print("tf: %s" % tf)
#     exit()

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

