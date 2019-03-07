import mysql.connector
from mysql.connector import errorcode

class MysqlAdapter:
    """
    MySQL datasource adapter.
    """
    # TODO support connection pooling

    def __init__(self, **config):
        self.config = config
        try:
            self.conn = mysql.connector.connect(**config)
            self.cur = self.conn.cursor()
        except mysql.connector.Error as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def get_cursor(self):
        """
        Return next row in query execution.
        execute_query() should be executed before calling this method.
        :return: next query result row.
        """
        return self.cur

    def execute_query(self, query_string):
        """
        Query a database table.
        :param query_string: query string to execute.
        :return: list of column names.
        """
        if self.cur is None:
            return None
        else:
            self.cur.execute(query_string)
            field_names = [i[0] for i in self.cur.description]
            return field_names

    def fetch_row(self):
        if self.cur is None:
            return None
        else:
            return self.cur.fetchone()

    def close_cursor(self):
        """
        Close query execution cursor and connection.
        """
        try:
            self.cur.close()
            self.conn.close()
        except:
            pass


if __name__ == '__main__':
    config = {'host': 'localhost', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    sql = 'SELECT * FROM orders'

    adapter = MysqlAdapter(**config)
    rows = adapter.execute_query(sql)
    print(rows)
    adapter.close_cursor()

