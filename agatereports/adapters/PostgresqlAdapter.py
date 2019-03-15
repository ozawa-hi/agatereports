import psycopg2
from psycopg2.extras import DictCursor

import logging
logger = logging.getLogger(__name__)


class PostgresqlAdapter:
    """
    Postgresql datasource adapter.
    """

    # TODO support connection pooling
    # TODO implement bulk read

    def __init__(self, dsn):
        self.config = dsn
        try:
            self.conn = psycopg2.connect(self.config)
            # self.cur = self.conn.cursor()
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        except psycopg2.OperationalError as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            logger.error('Operational error occurred connecting to Postgresql database.', exc_info=True)
        except psycopg2.Error as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            logger.error('unable to connect to Postgresql database. internal database connection error.', exc_info=True)

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
            try:
                self.cur.execute(query_string)
                field_names = [i[0] for i in self.cur.description]
                return field_names
            except psycopg2.ProgrammingError as err:
                logging.error('Specified user does not have privilege to query the database table.', exc_info=True)
                return None
            except psycopg2.Error as err:
                logging.error('Unable to query the database table.', exc_info=True)

    def fetch_row(self):
        if self.cur is None:
            return None
        else:
            try:
                return self.cur.fetchone()
            except psycopg2.ProgrammingError as err:
                return None
            except psycopg2.Error as err:
                return None

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
    logging.basicConfig(level=logging.INFO)

    config = {"adapter": "postgres",
              "config": "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"}
    sql = 'SELECT * FROM orders'

    adapter = PostgresqlAdapter(config.get('config'))
    rows = adapter.execute_query(sql)

    logging.info(rows)
    adapter.close_cursor()

