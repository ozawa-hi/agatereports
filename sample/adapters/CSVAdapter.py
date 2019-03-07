import csv


class CSVAdapter:
    """
    CSV datasource adapter.
    """
    def __init__(self, filename):
        try:
            self.csv_file = open(filename, 'r')
            self.csv_reader = csv.reader(self.csv_file)
            # self.csv_reader = csv.DictReader(self.csv_file)
        except IOError as err:
            if 'csv_file' in locals():
                self.csv_file.close()
            print(err)

    def get_cursor(self):
        """
        Return next row in query execution.
        execute_query() should be executed before calling this method.
        :return: next query result row.
        """
        return next(self.csv_reader)
        # return None

    def execute_query(self, query_string):
        """
        Query a database table.
        :param query_string: query string to execute.
        :return: list of column names.
        """
        if self.csv_reader is None:
            return None
        else:
            return next(self.csv_reader)

    def fetch_row(self):
        if self.csv_reader is None:
            return None
        else:
            try:
                return next(self.csv_reader)
            except StopIteration as err:
                return None
            except csv.Error:
                return None

    def close_cursor(self):
        """
        Close query execution cursor and connection.
        """
        if 'csv_file' in locals():
            self.csv_file.close()


if __name__ == '__main__':
    input_filename = '../../tests/data/address.csv'

    adapter = CSVAdapter(input_filename)
    header = adapter.execute_query('')
    print(header)
    adapter.close_cursor()

