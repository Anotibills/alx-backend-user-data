#!/usr/bin/env python3
"""
Implement the format method to filter values in incoming log records
Implement a function that takes no arguments and returns an object
Implement a get_db function that returns a connector to the database
Implement a main function that takes no arguments and returns nothing

"""
from typing import List
import logging
import re
from mysql.connector import connect, MySQLConnection
from os import environ

PII_FIELDS = ('name', 'email', 'password', 'ssn', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''
    This returns the log message obfuscated
    '''
    for field in fields:
        message = re.sub(rf'({field}=)[^{separator}]*({separator})',
                         rf'\1{redaction}\2', message)
    return message


def get_logger() -> logging.Logger:
    '''
    This returns logger obj
    '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> MySQLConnection:
    '''
    This connect to MySQL server with environmental vars
    '''
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    connector = connect(
        user=username,
        password=password,
        host=db_host,
        database=db_name)
    return connector


class RedactingFormatter(logging.Formatter):
    '''
    This redacting Formatter class
    '''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        This initializes class instance
        '''
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        This filters values in incoming log records
        '''
        return filter_datum(
            self.fields, self.REDACTION, super().format(record),
            self.SEPARATOR)


def main() -> None:
    '''
    This obtains a database connection using get_db and retrieve all
    '''
    db = get_db()
    cur = db.cursor()

    query = ('SELECT * FROM users;')
    cur.execute(query)
    fetch_data = cur.fetchall()

    logger = get_logger()

    for row in fetch_data:
        fields = '; '.join(
            f"{field}={value}" for field, value in zip(PII_FIELDS, row)
        )
        logger.info(fields)

    cur.close()
    db.close()


if __name__ == "__main__":
    main()
