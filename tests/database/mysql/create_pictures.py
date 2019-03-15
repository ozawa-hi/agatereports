import mysql.connector

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_table():
    """
    Create database table
    :return: if table was successfully created. True if created, False otherwise
    """
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # create database table
        cursor.execute("CREATE TABLE `agatereports`.`pictures` (`id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                       " `photos` BLOB NOT NULL)")
        cursor.close()
        conn.commit()
        logger.info("table 'agatereports`.`picture` created.")
        return True
    except mysql.connector.Error as err:
        if err.errno == 1050:
            logger.error("database table `agatereports`.`pictures` already exists. Recreating table.")
            drop_table()
        else:
            logger.error("Failed to create database table `agatereports`.`pictures`", err)
        return False
    finally:    # close database connection
        if conn.is_connected():
            conn.close()


def drop_table():
    """
    Create database table
    :return: if table was successfully created. True if created, False otherwise
    """
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # drop database table
        cursor.execute("DROP TABLE `agatereports`.`pictures`")
        cursor.close()
        conn.close()
        logger.info("table 'agatereports`.`picture` dropped.")
        return True
    except mysql.connector.Error as error:
        logger.error("Failed to create database table `agatereports`.`pictures`", error)
        return False
    finally:    # close database connection
        if conn.is_connected():
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
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        sql_insert_blob_query = """ INSERT INTO `pictures`
                          (`id`, `photos`) VALUES (%s,%s)"""
        pic = readImageFileFromDisk(photo)

        insert_blob_tuple = (row_id, pic)   # Convert data into tuple format
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        cursor.close()
        conn.commit()
        logger.info("Image and file inserted successfully as a BLOB into agatereports.picture table")
        return True
    except mysql.connector.Error as error:
        conn.rollback()
        logger.error("Failed inserting BLOB data into MySQL table {}".format(error))
        drop_table()
        return False
    finally:
        # closing database connection.
        if conn.is_connected():
            conn.close()


if __name__ == '__main__':
    """
    Create database table 'agatereports`.`pictures` that is used in a demo script.
    """
    config = {'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python',
              'database': 'agatereports'}
    if not create_table():
        create_table()
    filename = 'photo'
    for index in range(1, 6):
        name = '../../../demos/data/' + filename + '_' + str(index) + '.jpg'
        if not insertBLOB(index, name):     # if there is an insert error, quit
            break
