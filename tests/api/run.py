import unittest

# Django settings for testbackend project.
def hack_path():
    import os, sys
    common_path = os.path.join(os.path.abspath(os.path.dirname(".")), "..")
    sys.path.append(common_path)

hack_path()
from dbsettings import *

from sqlserver_ado import dbapi
import dbapi20

class test_dbapi(dbapi20.DatabaseAPI20Test):
    driver = dbapi
    connect_args = [ make_connection_string() ]
    
    def _try_run(self, *args):
        con = self._connect()
        cur = None
        try:
            cur = con.cursor()
            for arg in args:
                cur.execute(arg)
        finally:
            try:
                if cur is not None:
                    cur.close()
            except: pass
            con.close()

    def _try_run2(self, cur, *args):
        for arg in args:
            cur.execute(arg)
    
    # This should create the "lower" sproc.
    def _callproc_setup(self):
        self._try_run(
            """IF OBJECT_ID(N'[dbo].[to_lower]', N'P') IS NOT NULL DROP PROCEDURE [dbo].[to_lower]""",
            """
CREATE PROCEDURE to_lower
    @input nvarchar(max)
AS
BEGIN
    select LOWER(@input)
END
""",
            )
    
    # This should create a sproc with a return value.
    def _retval_setup(self, cur):
        self._try_run2(cur,
            """IF OBJECT_ID(N'[dbo].[add_one]', N'P') IS NOT NULL DROP PROCEDURE [dbo].[add_one]""",
            """
CREATE PROCEDURE add_one (@input int)
AS
BEGIN
    return @input+1
END
""",
            )

    def test_retval(self):
        con = self._connect()
        try:
            cur = con.cursor()
            self._retval_setup(cur)
            values = cur.callproc('add_one',(1,))
            self.assertEqual(values[0], 1, 'input parameter should be left unchanged: %s' % (values[0],))
            
            self.assertEqual(cur.description, None,"No resultset was expected.")
            self.assertEqual(cur.return_value, 2, "Invalid return value: %s" % (cur.return_value,))

        finally:
            con.close()

    # This should create a sproc with an output parameter.
    def _outparam_setup(self, cur):
        self._try_run2(cur,
            """IF OBJECT_ID(N'[dbo].[add_one_out]', N'P') IS NOT NULL DROP PROCEDURE [dbo].[add_one_out]""",
            """
CREATE PROCEDURE add_one_out (@input int, @output int OUTPUT)
AS
BEGIN
    SET @output = @input+1
END
""",
            )

    def test_outparam(self):
        con = self._connect()
        try:
            cur = con.cursor()
            self._outparam_setup(cur)
            values = cur.callproc('add_one_out',(1,None))
            self.assertEqual(len(values), 2, 'expected 2 parameters')
            self.assertEqual(values[0], 1, 'input parameter should be unchanged')
            self.assertEqual(values[1], 2, 'output parameter should get new values')
        finally:
            con.close()            
    
    # Don't need exceptions mirrored on connections.
    def test_ExceptionsAsConnectionAttributes(self): 
        pass
        
    # Don't need setoutputsize tests.
    def test_setoutputsize(self): 
        pass
        
    def help_nextset_setUp(self,cur):
        self._try_run2(cur,
            """IF OBJECT_ID(N'[dbo].[more_than_one]', N'P') IS NOT NULL DROP PROCEDURE [dbo].[more_than_one]""",
            """
create procedure more_than_one
as
begin
    select 1,2,3
    select 4,5,6
end
""",
            )

    def help_nextset_tearDown(self,cur):
        pass
   
suite = unittest.makeSuite(test_dbapi, 'test')
testRunner = unittest.TextTestRunner(verbosity=9)
print testRunner.run(suite)
