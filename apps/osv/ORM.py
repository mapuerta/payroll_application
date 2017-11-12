from utils.Adapterdb import init_connector_db as _cursor
import fields
import json
from base.base import base_tables, property_table
from datetime import datetime

LOG_ACCESS_COLUMNS = ['create_uid', 'create_date', 'write_uid', 'write_date']
MAGIC_COLUMNS = ['id'] + LOG_ACCESS_COLUMNS
ENVIRONMENT = {}
FIELD_ATTRS = ["index", "required", "size", "compute", "unique", "default"]

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
    _last_login = False
    _colums = {}
    _constraint = []
    
    def __init__(self):
        self._table = self._name.replace(".", "_")
        self._cr = _cursor()
        self._uid = self._last_login or 1
        self.id = self._cr.last_row_id
        self.env = ENVIRONMENT
        self._init_base_tables()
        self._auto_init()

    @property
    def active_id(self):
        return self._cr.last_row_id

    def _init_base_tables(self):
        for table, sql in base_tables.items():
            exists = self._table_exist(table=table)
            if exists:
                continue
            self._cr.execute(sql)

    def get_fields_changes(self):
        sql = """select name, type, attr, change from ir_model_change
                 where model='%s'"""
        return self._cr.execute(sql%self._table)
        
    def get_fields_exists(self, name):
        sql = """select id, name, type, attrs from
                 ir_fields where name="%s" and model="%s"
              """%(name, self._table)
        rows = self._cr.execute(sql)
        return rows

    def register_fields(self, name, value, field_attrs, add_new=False):
        _attrs = {}
        change = False
        query = """INSERT INTO ir_fields (name, type, model, attrs)
                   VALUES ("%s", "%s", "%s", "%s");"""
        ir_field = self.get_fields_exists(name)
        for attr in FIELD_ATTRS:
            if hasattr(field_attrs, attr):
                _attrs[attr] = getattr(field_attrs, attr)
        columms = {"name": name, "type": value, "attrs": _attrs.items()}
        if not ir_field or add_new:
            if not add_new:
                self._cr.execute(query%(name, value, self._table, _attrs.items()))
            sql = self.add_columns_model(name, value, _attrs)
            self._cr.execute(sql)
            return False
        id, field, type, attrs = ir_field[0]
        columms["name"] = field
        columms["type"] = value
        columms["attrs"] = _attrs.items()
        attrs = dict(eval(attrs))
        new_attrs = {}
        for key in attrs:
            if _attrs[key] != attrs[key]:
                new_attrs[key] = _attrs[key]
        if type != value and not new_attrs:
            new_attrs = attrs
        if not new_attrs and type == value:
            return 
        self.update_ir_field(columms, id)
        self.save_changes_model(name, value, new_attrs)

    def update_ir_field(self, change, model_id):
        sql = "update ir_fields set "
        changes = []
        for column, value in  change.items():
            field = '%s="%s"'%(column, value)
            changes.append(field)
        sql +=", ".join(changes)
        sql +=" where id=%s;"%model_id
        self._cr.execute(sql)

    def save_changes_model(self, field, type, updates):
        query = """INSERT INTO ir_model_change(name, type, model, attr, CHANGE)
                   VALUES('%s', '%s', '%s', '%s', '%s')"""
        for attr, value in updates.items():
            self._cr.execute(query%(field, type, self._table, attr, str(value)))

    def add_propertys(self, attrs):
        add_attrs = []
        for key, value in attrs.items():
            if key in property_table and value:
                add_attrs.append('%s'%property_table[key].format(value))
        return " ".join(add_attrs)
        
    def add_columns_model(self, name, type, attrs):
        sql = 'ALTER TABLE "%s" ADD COLUMN "%s" "%s" '%(self._table,  name, type)
        sql += self.add_propertys(attrs)
        return sql
        
    def update_columns_model(self):
        temp_name = "temp_{}".format(self._table)
        changes = self.get_fields_changes()
        rename = "alter table %s rename to %s"%(self._table, temp_name)
        copy = "INSERT INTO %s %s SELECT %s FROM %s;"
        if not changes:
            return
        self._cr.execute(rename)
        create = self._create_table()
        for field, value in self._columns.items():
            self.register_fields(field, value.column_type[0], value, add_new=True)
        values = ', '.join('"%s"' % c for c in self._columns)
        value_insert = "("+values+")"
        self._cr.execute(copy%(self._table, value_insert, values, temp_name))
        self._cr.execute("DROP TABLE %s"%temp_name)
        self._cr.execute("DELETE FROM ir_model_change where model='%s'"%self._table)

    def _table_exist(self, table=False):
        table = table or self._table
        query = "select DISTINCT tbl_name from sqlite_master where TYPE='table' AND  tbl_name='%s'"
        cursor = self._cr.execute(query%(table,))
        return cursor

    def _create_table(self):
        columns_propertys = {}
        for magic in MAGIC_COLUMNS:
            default_type = "INTEGER"
            if magic == 'id':
                default_type += " PRIMARY KEY AUTOINCREMENT"
            if magic.endswith("_date"):
                default_type = " TEXT"
            columns_propertys[magic] = default_type
        sql = ", ".join('%s %s'%(colm, attr) for colm, attr in columns_propertys.items())
        sql = "({0})".format(sql)
        sql = 'CREATE TABLE "%s" %s'%(self._table, sql)
        self._cr.execute(sql)

    def _auto_init(self):
        create = self._table_exist()
        if not create:
            self._create_table()
        self._add_fields()

    def _add_fields(self):
        for field, value in self._columns.items():
            self.register_fields(field, value.column_type[0], value)
        self.update_columns_model()

    def _create(self, vals):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vals.update({"create_uid": self._uid, "create_date": "'%s'"%now})
        query = """INSERT INTO "%s" (%s) VALUES(%s)""" % (
            self._table,
            ', '.join('"%s"' % u[0] for u in vals.items()),
            ', '.join(str(u[1]) for u in vals.items()),
            )
        self._cr.execute(query)
        self.id = self._cr.last_row_id

    def create(self, values):
        self._create(values)
        return self

    def _write(self, vals, model_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vals.update({"write_uid": self._uid, "write_date": "'%s'"%now})
        query = 'UPDATE "%s" SET %s WHERE id = %s' % (
                self._table, ','.join('"%s"=%s' % (u[0], u[1]) for u in vals.items()),
                model_id)
        self._cr.execute(query)

    def write(self, values, model_id=False):
        model_id = self.id or model_id
        self._write(values, model_id)
        return self

    def _delete(self, model_ids):
        if not isinstance(model_ids, list):
            model_ids = [model_ids]
        for sub_id in model_ids:
            query = "DELETE FROM %s WHERE id = %s" %(self._table, sub_id)
            self._cr.execute(query)

    def delete(self, model_id=False):
        model_id = model_id or self.active_id or self.id
        self._delete(model_id)
        return self

    def search(self, domain, limit=None, order=None):
        pass
        
