import psycopg2

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_table():
    """
    Create database table
    :return: if table was successfully created. True if created, False otherwise
    """
    conn = None
    try:
        conn = psycopg2.connect(config)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE pictures (id SERIAL PRIMARY KEY, photos BYTEA NOT NULL);")
        cursor.close()
        conn.commit()
        logger.info("table picture created.")
        return True
    except psycopg2.OperationalError as err:
        logger.error("Failed to create database table `agatereports`.`pictures`", err)
        return False
    except psycopg2.ProgrammingError as err:
        if err.pgcode == '42P07':
            drop_table()
        return False
    except psycopg2.Error as err:
        logger.error('unable to connect to Postgresql database. internal database connection error.', err.pgerror)
        return False
    finally:    # close database connection
        if conn is not None:
            conn.close()


def drop_table():
    """
    Create database table
    :return: if table was successfully created. True if created, False otherwise
    """
    conn = None
    try:
        conn = psycopg2.connect(config)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE pictures")
        cursor.close()
        conn.commit()
        logging.info("table picture dropped.")
        return True
    except psycopg2.OperationalError as err:
        logging.error("Failed to create database table pictures", err.pgerror)
        return False
    finally:    # close database connection
        if conn is not None:
            conn.close()


def readImageFileFromDisk(filename):
    """
    Convert digital data to binary format
    :param filename: file to convert
    :return: binary data content of specified file
    """
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(row_id, photo):
    """
    Insert binary file content to database table 'agatereports`.`pictures`.
    :param row_id: row number to insert into
    :param photo: binary image file
    """
    conn = None
    try:
        conn = psycopg2.connect(config)
        cursor = conn.cursor()

        sql_insert_blob_query = """ INSERT INTO pictures
                          (id, photos) VALUES (%s,%s)"""
        pic = readImageFileFromDisk(photo)

        insert_blob_tuple = (row_id, pic)   # Convert data into tuple format
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        cursor.close()
        conn.commit()
        logger.info("Image and file inserted successfully as a BLOB into agatereports.picture table")
        return True
    except psycopg2.OperationalError as err:
        logger.error("Failed to insert BLOB data into PostgreSQL database table 'picture'.", err.pgerror)
        # drop_table()
        return False
    except psycopg2.ProgrammingError as err:
        logger.error("Failed to insert BLOB data into PostgreSQL database table 'picture'.", err.pgerror)
        # drop_table()
        return False
    except psycopg2.Error as err:
        logger.error('unable to connect to Postgresql database. internal database connection error.', err.pgerror)
        # drop_table()
        return False
    finally:    # close database connection
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    """
    Create database table 'agatereports`.`pictures` that is used in a demo script.
    """
    config = "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"
    if not create_table():
        create_table()

    filename = 'photo'
    for index in range(1, 6):
        name = '../../../demos/data/' + filename + '_' + str(index) + '.jpg'
        if not insertBLOB(index, name):     # if there is an insert error, quit
            break
