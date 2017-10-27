
def copy_list_dicts(lines):
    res = []
    for line in lines:
        dict_t = {}
        for keys in line.keys():
            dict_t.update({keys: line[keys]})
        res.append(dict_t.copy())
    return res

class PostgresConnector(object):
    __conn = None
    __cursor = None
    __allowed_keys = ['host', 'port', 'dbname', 'user', 'password']
    __str_conn = ''

    def __init__(self, config=None):
        if config is None:
            config = {}
        for key, value in config.items():
            if value is not None and key in self.__allowed_keys:
                self.__str_conn = '%s %s=%s' % (self.__str_conn, key, value)
            elif key == 'dbname' and value is None:
                self.__str_conn = '%s %s=%s' % (
                    self.__str_conn, 'dbname', 'postgres')
        logger.debug('Connection string: %s', self.__str_conn)
        try:
            logger.debug('Stabilishing connection with db server')
            self.__conn = psycopg2.connect(self.__str_conn)
            if config.get('isolation_level', False):
                self.__conn.set_isolation_level(0)
            self.__cursor = self.__conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
        except Exception as error:
            # TODO: log this then raise
            logger.debug(
                'Connection to database not established: %s', str(error))
            # Proper cleanup
            self.disconnect()
            raise

    def execute(self, sql_str, *args):
        change = sql_str.lower().startswith('insert into') or \
            sql_str.lower().startswith('update') or \
            sql_str.lower().startswith('create') or \
            sql_str.lower().startswith('delete') or \
            sql_str.lower().startswith('alter') or \
            sql_str.lower().startswith('reassign')
        try:
            logger.debug('SQL: %s', sql_str)
            self.__cursor.execute(sql_str, *args)
        except Exception:
            self.__conn.rollback()
            raise
        else:
            if change:
                self.__conn.commit()
        return copy_list_dicts(self.__cursor) if not change else True

    def check_config(self):
        """Check if can connect to PostgreSQL server with the provided configuration.

        :returns: If succeeded or not.
        :rtype: bool
        """
        try:
            logger.debug('')
            res = self.execute("select version();")
            logger.debug('Postgres returned: %s', res)
        except Exception as error:  # pylint: disable=W0703
            logger.error('PostgreSQL connection test failed %s',
                         str(error))
            return False
        return True

    def disconnect(self):
        if self.__cursor:
            logger.debug('disconnect: closing cursor')
            self.__cursor.close()
        if self.__conn:
            logger.debug('disconnect: closing connection')
            self.__conn.close()

    def __del__(self):
        self.disconnect()

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def __enter__(self):
        return self        
        
