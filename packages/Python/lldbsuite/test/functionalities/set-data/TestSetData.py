"""
Set the contents of variables and registers using raw data
"""

from __future__ import print_function

import use_lldb_suite

import os, time
import lldb
from lldbsuite.test.lldbtest import *
import lldbsuite.test.lldbutil as lldbutil

class SetDataTestCase(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    @skipUnlessDarwin
    def test_set_data(self):
        """Test setting the contents of variables and registers using raw data."""
        self.build()
        exe = os.path.join(os.getcwd(), "a.out")
        self.runCmd("file " + exe, CURRENT_EXECUTABLE_SET)

        self.runCmd("br s -p First");
        self.runCmd("br s -p Second");

        self.runCmd("run", RUN_SUCCEEDED)

        self.expect("p myFoo.x", VARIABLES_DISPLAYED_CORRECTLY,
            substrs = ['2'])

        process = self.dbg.GetSelectedTarget().GetProcess()
        frame = process.GetSelectedThread().GetFrameAtIndex(0)

        x = frame.FindVariable("myFoo").GetChildMemberWithName("x")

        my_data = lldb.SBData.CreateDataFromSInt32Array(lldb.eByteOrderLittle, 8, [4])
        err = lldb.SBError()

        self.assertTrue (x.SetData(my_data, err))

        self.runCmd("continue")

        self.expect("p myFoo.x", VARIABLES_DISPLAYED_CORRECTLY,
            substrs = ['4'])

        frame = process.GetSelectedThread().GetFrameAtIndex(0)

        x = frame.FindVariable("string")

        if process.GetAddressByteSize() == 8:
            my_data = lldb.SBData.CreateDataFromUInt64Array(process.GetByteOrder(), 8, [0])
        else:
            my_data = lldb.SBData.CreateDataFromUInt32Array(process.GetByteOrder(), 4, [0])
        
        err = lldb.SBError()

        self.assertTrue (x.SetData(my_data, err))

        self.expect("fr var -d run-target string", VARIABLES_DISPLAYED_CORRECTLY,
            substrs = ['NSString *', 'nil'])