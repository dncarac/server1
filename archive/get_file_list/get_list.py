#! ./venv/Scripts python
# coding: utf-8
''' get_file_list.py --

@summary: module_summary

@description: module_detailed_description

__Created__ = "2019-04-18"
__Updated__ = "2019-04-18"

@author: Den
@copyright: Copyright © 2019 Den
@License: ALL RIGHTS RESERVED
'''    # region - logging setup
import logging

import requests

logging.basicConfig()
_LOG = logging.getLogger("get_file_list.get_list -- ")
# _LOG.level = logging.INFO
# _LOG.level = logging.TRACE
# endregion

r = requests.get("http://type-lines.com")
print(r)
lst = r.text
print(lst)
