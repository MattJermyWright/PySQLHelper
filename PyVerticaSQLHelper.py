#!/usr/bin/env python

import vertica_python
import PySQLHelper


class PyVerticaSQLHelper(PySQLHelper.PyBaseSQLHelper):
    def __init__(self, connectionString):
        PySQLHelper.PyBaseSQLHelper.__init__(self, connectionString)

    def connect(self):
        self.connection = vertica_python.connect(**self.connectionString)

    def executeFetchall(self, sql):
        sql = PySQLHelper.PyBaseSQLHelper.helperConnectAndPrepSQL(self, sql)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


def main():
    connectString = {
        'host': '',  # Hostname goes here
        'port': 5433,  # Standard vertica port
        'user': '',  # Username goes here
        'password': '',  # Password goes here
        'database': '',
        'read_timeout': 600  # Used for default timeouts
    }
    sqlVariables = {
        'DATERANGE': ' visit_day between 20161201 and 20161201'  # Substituted across all SQL statements
    }
    queries = {
        'testSQL': """SELECT count(DISTINCT visitor_id) FROM hpcom.omni_hit WHERE {DATERANGE} """,
        'testFile': """testfile.sql"""
    }
    sqlEngine = PyVerticaSQLHelper(connectString)
    sqlEngine.autobindingVariables = sqlVariables
    results1 = sqlEngine.executeFetchall(queries['testSQL'])
    results2 = sqlEngine.executeFetchallFile(queries['testFile'], True)

    print("Results: " + str([results1, results2]))

if __name__ == "__main__":
    main()
