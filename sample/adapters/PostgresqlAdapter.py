import psycopg2
from psycopg2.extras import DictCursor

class PostgresqlAdapter:
    """
    Postgresql datasource adapter.
    """

    # TODO support connection pooling

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
            print(err)
        except psycopg2.Error as err:
            self.close_cursor()
            self.conn = None
            self.cur = None
            print('unable to connect to Postgresql database. internal database connection error.', err)

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
                print('Specified user does not have privilege to query the database table.', err)
                return None
            except psycopg2.Error as err:
                print('Unable to query the database table.', err)

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
    config = "host='172.17.0.2' port='5432' dbname='agatereports' user='python' password='python'"
    sql = 'SELECT * FROM orders'

    adapter = PostgresqlAdapter(config)
    rows = adapter.execute_query(sql)

    print(rows)
    adapter.close_cursor()

