import mysql.connector
from mysql.connector import errorcode

import logging
logger = logging.getLogger(__name__)


class MysqlAdapter:
    """
    MySQL datasource adapter.
    """
    # TODO support connection pooling
    # TODO implement bulk read

    def __init__(self, **config_list):
        self.config = config_list
        try:
            self.conn = mysql.connector.connect(**config_list)
            self.cur = self.conn.cursor()
        except mysql.connector.Error as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Unable to access MySQL database with provided user/password.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error('Specified MySQL database does not exist')
            else:
                logger.error('Failed to connect to MySQL database', exc_info=True)
        except AttributeError as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            print('invalid connection configuration:' + str(self.config))

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
        except Exception:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    config = {'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    sql = 'SELECT * FROM orders'

    adapter = MysqlAdapter(**config)
    rows = adapter.execute_query(sql)
    logger.info(rows)
    adapter.close_cursor()

