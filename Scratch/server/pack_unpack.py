# -*- coding: utf-8 -*-
''' Scratch.pack_unpack -

@summary: Test module for _pack/_unpack

@description: Contains two functions

__CreatedOn__="2020-03-08"
__UpdatedOn__="2020-04-15"

@version: 0.1
@author: Den
@copyright: Copyright © 2020 Den
@license: ALL RIGHTS RESERVED
'''
from TaskData import *    # @UnusedWildImport
import pprint
# region - logging setup
import logging    # @Reimport
logging.basicConfig()
_LOG = logging.getLogger(__name__)
# _LOG.level = logging.INFO
# _LOG.level = logging.TRACE
# endregion


def p_packtd):
    ''' p_pack--
    '''
    _LOG.trace("Enter p_packwith:\n%s" % td)
#------------------------------------------------------------------------------
    fil = "TaskData(\n"
    for f, ff in zip(td, fields(td)):
        fil += "%s=%s\n" % (ff.name, repr(f))
    fil += ")"
#------------------------------------------------------------------------------
    _LOG.trace("Leave p_packreturning:\n%s" % fil)
    return fil


def u_unpackfil):
    ''' method --
    '''
    _LOG.trace("Enter method with fil:\n%s" % fil)
#------------------------------------------------------------------------------
    current_classes = [cls.__name__ for cls in DataClass.__subclasses__()]
    tdr = ""
    for l in fil.splitlines():
        m = l[l.find("=") : l.find("(")][1:]
        if m == "": tdr += l
        if m in current_classes: tdr += l + ","
        m += "\n"
    td = eval(tdr)
#------------------------------------------------------------------------------
    _LOG.trace("Leave method returning td:\n%s" % td)
    return td


if __name__ == '__main__':
    print("Start\n")

#   Quick test ----------------------------------------------------------------
    td = TaskData()
    fil = p_packtd)
    td2 = unpack(fil)
    assert td2 == td

#   Augmented file ------------------------------------------------------------
    lst = fil.splitlines()
    lst.insert(2, "additional_data=AddnData(first=1, second2)")
    aug_fil = ""
    for l in lst: aug_fil += l + "\n"
    td4 = unpack(aug_fil)
    assert td4 == td

#   Diinished file ------------------------------------------------------------
    lst = fil.splitlines()
    del lst[2:3]
    dim_fil = ""
    for l in lst: dim_fil += l + "\n"
    lst = fil.splitlines()

    td5 = unpack(dim_fil)
    assert td5 == td

    print("\nDone")
