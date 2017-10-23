
from utils.Adapterdb import init_connector_db as _cursor
import fields
import json

LOG_ACCESS_COLUMNS = ['create_uid', 'create_date', 'write_uid', 'write_date']
MAGIC_COLUMNS = ['id'] + LOG_ACCESS_COLUMNS
ENVIRONMENT = {}
FIELD_ATTRS = ["index", "required", "readonly", "size", "compute"]

class Meta(type):

    def __init__(self, name, bases, attrs):
        if not self._register:
            self._register = True
            super(Meta, self).__init__(name, bases, attrs)
            return

    def __call__(cls, *args, **kwargs):
        ENVIRONMENT.update({cls._name: cls})
        return super(Meta, cls).__call__(*args, **kwargs)


class BaseModel(object):
    __metaclass__ = Meta
    _name = "base"
    _description = "description"
    _register = False
    _colums = {}
    
    def __init__(self):
        self._table = self._name.replace(".", "_")
        self._cr = _cursor()
        self.env = ENVIRONMENT
        self._auto_init()
        
    def _cretae_table_fields(self):
        table = "ir_fields"
        create = self._table_exist(table=table)
        if create:
            return
        sql = """
              CREATE TABLE "%s"
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT NOT NULL,
                TYPE TEXT NOT NULL,
                MODEL TEXT NOT NULL,
                ATTRS TEXT NOT NULL);
            """
        self._cr.execute(sql%(table,))

    def get_fields_exists(self, name):
        sql = """select id, name, type, attrs from
                 ir_fields where name="%s" and model="%s"
              """%(name, self._table)
        rows = self._cr.execute(sql)
        return rows
        
    def register_fields(self, name, value, field_attrs):
        _attrs = {}
        query = """INSERT INTO ir_fields (name, type, model, attrs)
                   VALUES ("%s", "%s", "%s", "%s");"""
        ir_field = self.get_fields_exists(name)
        for attr in FIELD_ATTRS:
            if hasattr(field_attrs, attr):
                _attrs[attr] = getattr(field_attrs, attr)
        columms = {"name": name, "type": value, "attrs": _attrs.items()}
        if not ir_field:
            self._cr.execute(query%(name, value, self._table, _attrs.items()))
            self.update_columns_model(name, value, _attrs)
            return True
        id, field, type, attrs = ir_field[0]
        columms["name"] = field
        columms["type"] = type
        columms["attrs"] = attrs
        self.update_ir_field(columms, id)
        attrs = dict(eval(attrs))
        new_attrs = {}
        for key in attrs:
            if _attrs[key] != attrs[key]:
                new_attrs[key] = _attrs[key]
        self.update_columns_model(name, value, new_attrs, False)

    def update_ir_field(self, change, id):
        sql = "update ir_fields set "
        for key, value in change.items():
            sql += "%s='%s'\n"%(key, value)
        sql += "where id=%s;"
        #~ self._cr.execute(sql)

    def update_columns_model(self, name, type, attrs, add=True):
        if add:
            sql = 'ALTER TABLE "%s" ADD COLUMN "%s" "%s" "%s"'
        

    def _table_exist(self, table=False):
        table = table or self._table
        query = "select DISTINCT tbl_name from sqlite_master where TYPE='table' AND  tbl_name='%s'"
        cursor = self._cr.execute(query%(table,))
        return cursor

    def _create_table(self):
        self._cr.execute('CREATE TABLE "%s" (ID INTEGER PRIMARY KEY AUTOINCREMENT)' % (self._table,))

    def _auto_init(self):
        create = self._table_exist()
        if not create:
            self._create_table()
        self._add_fields()

    def _add_fields(self):
        self._cretae_table_fields()
        for field, value in self._columns.items():
            self.register_fields(field, value.column_type, value)
            
        #~ for field, value in self._columns.items():
            #~ sql = 'ALTER TABLE "%s" ADD COLUMN "%s" "%s" "%s"'
            #~ self._cr.execute(sql %(self._table, field, value.column_type, value.not_null))

class A(BaseModel):
    _name = "model.a"
    _columns = {
        "user": fields.Char(string="user", required=True, size=20),
        "user2": fields.Text(string="name", required=True, intex=True),
        "cedula": fields.Text(string="name", required=True, intex=True),
    }

    def pp(self):
        print self.env

a = A()
#~ print a.user

