#!/usr/bin/env python

import getopt
import sys
import os
import re

debugFlag = False


def pdebug(str):
    global debugFlag
    if debugFlag:
        print("***DEBUG: " + str)


def processOptions():
    argv = sys.argv

    def helpInfo():
        print('Usage: {} [-h|--help] [-d|--debug]'.format(sys.argv[0]))
        sys.exit(2)

    global debugFlag
    try:
        opts, args = getopt.getopt(argv[1:], "h:d", ["help", "debug"])
    except getopt.GetoptError:
        helpInfo()
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            helpInfo()
        elif opt in ["-d", "--debug"]:
            debugFlag = True


class PyBaseSQLHelper:
    def __init__(self, connectionString):
        self.connectionString = connectionString
        self.connection = None
        self.autobindingVariables = None

    def connect(self):
        pdebug("Connecting: Inside PyBaseSQLHelper")
        pass

    def helperConnectAndPrepSQL(self, sql):
        pdebug("connectAndPrepSQL: Inside PyBaseSQLHelper")
        if self.connection is None:
            pdebug("connectAndPrepSQL: No connection yet...connecting")
            self.connect()
        if self.autobindingVariables is not None:
            pdebug("connectAndPrepSQL: Processing SQL Formatter against bind variables: "
                   + str(self.autobindingVariables))
            sql = sql.format(**self.autobindingVariables)
        return sql

    def helperReadSQLFile(self, filename, fixParameters=True, regExpParamToMatch=r':variable(\w+)'):
        def fixParameterValues(sqlString):
            return re.sub(regExpParamToMatch, r'{\1}', sqlString)

        if filename.find("/") > 0 or filename.find('\\') > 0:
            pdebug("readSQLFile: Adding CWD to filename due to relative pathing")
            filename = os.path.join(os.getcwd(), filename)
        with open(filename, "r") as fp:
            pdebug("readSQLFile: Reading SQL file...")
            sql = fp.read()
            if fixParameters:
                sql = fixParameterValues(sql)
            return sql

    def executeFetchall(self, sql):
        sql = PyBaseSQLHelper.helperConnectAndPrepSQL(self, sql)
        pdebug("PyBaseSQLHelper:executeFetchall: Final SQL: " + sql)
        return None

    def executeFetchallFile(self, sqlFile, fixParameters):
        pdebug("PyBaseSQLHelper:executeFetchallFile: Final SQL: " + sqlFile)
        return self.executeFetchall(self.helperReadSQLFile(sqlFile, fixParameters))


class PyDummySQLHelper(PyBaseSQLHelper):
    def __init__(self, connectionString):
        PyBaseSQLHelper.__init__(self, connectionString)

    def connect(self):
        pdebug("Inside PyDummySQLHelper:connect")

    def executeFetchall(self, sql):
        pdebug("Inside PyDummySQLHelper:executeFetchall")
        sql = PyBaseSQLHelper.helperConnectAndPrepSQL(self, sql)
        pdebug("PyDummySQLHelper:executeFetchall: Final SQL: " + sql)
        return [["Dummy SQL Helper Working OK:" + sql]]


def main():
    connectString = {  # Includes all of the connection information used when connecting to the system
        'host': 'localhost',
        'port': 5433,
        'user': 'id goes here',
        'password': 'password goes here',
        'database': 'database name',
        'read_timeout': 600
    }
    sqlVariables = {
        # Automatically replace all :variable or :parameter markup with comparable value names defined here
        'DATE_RANGE': ' visit_day between 20161201 and 20161201'
    }
    queries = {  # Series of queries to use - illustrates test cases only
        'testSQL': """SELECT count(DISTINCT visitor_id)
                        FROM hpcom.omni_hit
                        WHERE {DATE_RANGE} """,
        'testFile': "testfile.sql"  # Filename example, assume relative directories unless a leading / or \
    }
    ## TEST DUMMY DRIVER
    sqlEngine = PyDummySQLHelper(connectString)
    sqlEngine.autobindingVariables = sqlVariables
    results1 = sqlEngine.executeFetchall(queries['testSQL'])
    results2 = sqlEngine.executeFetchallFile(queries['testFile'], True)

    print("Results: " + str([results1, results2]))


if __name__ == "__main__":
    processOptions()
    main()
