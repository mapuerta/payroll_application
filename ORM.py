
from utils.Adapterdb import PostgresConnector

LOG_ACCESS_COLUMNS = ['create_uid', 'create_date', 'write_uid', 'write_date']
MAGIC_COLUMNS = ['id'] + LOG_ACCESS_COLUMNS


class Fields(object):

    def Text(self, name, description, required=False):
        column = [name, "TEXT"] + self.not_null(required)
        return column

    def Float(self, name, description, size=4, required=False):
        float_type = "float4"
        if size > 4:
            float_type = "float8"
        return [name, float_type] + self.not_null(required))

    def Date(self, name, description, required=False):
        type_value = "date"
        return [name, type_value] + self.not_null(required))

    def Datetime(self, name, description, required=False):
        type_value = "datetime"
        return [name, type_value] + self.not_null(required))

    def Char(self, name, description, size=100, required=False):
        type_value = "char({0})".format(size)
        return [name, type_value] + self.not_null(required))

    def Boolean(self, name, description, required=False):
        type_value = "boolean"
        return [name, type_value] + self.not_null(required))

    def Serial(self, name, description, required=False):
        type_value = "serial"
        return [name, type_value] + self.not_null(required))
        
    def Money(self, name, description, required=False):
        type_value = "money"
        return [name, type_value] + self.not_null(required))

    def Binary(self, name, description, required=False):
        type_value = "bytea"
        return [name, type_value] + self.not_null(required))

    def Integer(self, name, description, size=2, required=False):
        type_value = "int2"
        if size > 2 and size <=4:
            type_value = "int4"
        elif size > 4 and size <= 8:
            type_value = "int8"
        else:
            type_value = "int28"
        return [name, type_value] + self.not_null(required))

    def not_null(self, required):
        return ["NOT NULL"] if required else []

class BaseModel(PostgresConnector):
    _name = "base"
    _description = "description"
    
    def __init__(self):
        self._table = self._name

    def _table_exist(self):
        query = "SELECT relname FROM pg_class WHERE relkind IN ('r','v') AND relname=%s"
        self._cr.execute(query, (self._table,))
        return self._cr.rowcount

    def _create_table(self):
        self._cr.execute('CREATE TABLE "%s" (id SERIAL NOT NULL, PRIMARY KEY(id))' % (self._table,))
        self._cr.execute("COMMENT ON TABLE \"%s\" IS %%s" % self._table, (self._description,))


class Poller(PostgresConnector):

    def __init__(self, table):
        self.table = table
        self.id = False

    def create(self, vals):
        return self

    def update(self, ids, vals):
        return self

    def deleted(self, ids):
        return self

    def search(self, domain):
        return self

    def read(self, ids, fields):
        return self
