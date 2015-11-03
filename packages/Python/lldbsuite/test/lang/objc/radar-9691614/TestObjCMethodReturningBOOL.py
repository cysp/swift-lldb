"""
Test that objective-c method returning BOOL works correctly.
"""

from __future__ import print_function

import use_lldb_suite

import os, time
import lldb
from lldbsuite.test.lldbtest import *
import lldbsuite.test.lldbutil as lldbutil

@skipUnlessDarwin
class MethodReturningBOOLTestCase(TestBase):

    mydir = TestBase.compute_mydir(__file__)

    def setUp(self):
        # Call super's setUp().
        TestBase.setUp(self)
        # We'll use the test method name as the exe_name.
        self.exe_name = self.testMethodName
        # Find the line number to break inside main().
        self.main_source = "main.m"
        self.line = line_number(self.main_source, '// Set breakpoint here.')

    def test_method_ret_BOOL(self):
        """Test that objective-c method returning BOOL works correctly."""
        d = {'EXE': self.exe_name}
        self.build(dictionary=d)
        self.setTearDownCleanup(dictionary=d)

        exe = os.path.join(os.getcwd(), self.exe_name)
        self.runCmd("file " + exe, CURRENT_EXECUTABLE_SET)

        lldbutil.run_break_set_by_file_and_line (self, "main.m", self.line, num_expected_locations=1, loc_exact=True)

        self.runCmd("run", RUN_SUCCEEDED)
        self.expect("process status", STOPPED_DUE_TO_BREAKPOINT,
            substrs = [" at %s:%d" % (self.main_source, self.line),
                       "stop reason = breakpoint"])

        # rdar://problem/9691614
        self.runCmd('p (int)[my isValid]')