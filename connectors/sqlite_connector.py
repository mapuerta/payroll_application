import sqlite3
import logging

logger = logging.getLogger(__name__)


def copy_list_dicts(lines):
    res = []
    for line in lines:
        if isinstance(line, tuple):
            res.append(line)
            continue
        dict_t = {}
        for keys in line.keys():
            dict_t.update({keys: line[keys]})
        res.append(dict_t.copy())
    return res


class SqliteConnector(object):
    __dbname = None
    __cursor = None
    __conn = None

    def __init__(self, dbname):
        self.__conn = sqlite3.connect(dbname)

    def execute(self, sql_str, *args):
        change = sql_str.lower().startswith('insert into') or \
            sql_str.lower().startswith('update') or \
            sql_str.lower().startswith('delete') or \
            sql_str.lower().startswith('reassign')
        try:
            logger.debug('SQL: %s', sql_str)
            #~ import pdb;pdb.set_trace()
            self.__cursor = self.__conn.execute(sql_str, *args)
        except Exception as error:
            self.__conn.rollback()
            raise error
        else:
            if change:
                self.__conn.commit()
        return copy_list_dicts(self.__cursor) if not change else True


    def disconnect(self):
        if self.__conn:
            logger.debug('disconnect: closing connection')
            self.__conn.close()

    def __del__(self):
        self.disconnect()

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def __enter__(self):
        return self        

