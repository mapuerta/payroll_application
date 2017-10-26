from datetime import datetime, date
from misc import DATETIME_FORMAT, DATE_FORMAT, TIME_FORMAT
from misc import isBase64, encode_image, image_resize_image
DATE_LENGTH = len(date.today().strftime(DATE_FORMAT))
DATETIME_LENGTH = len(datetime.now().strftime(DATETIME_FORMAT))
Default = object()
EMPTY_DICT = {}

class MetaField(type):
    by_type = {}

    def __new__(meta, name, bases, attrs):
        base_slots = {}
        for base in reversed(bases):
            base_slots.update(getattr(base, '_slots', ()))

        slots = dict(base_slots)
        slots.update(attrs.get('_slots', ()))

        attrs['__slots__'] = set(slots) - set(base_slots)
        attrs['_slots'] = slots
        return type.__new__(meta, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        super(MetaField, cls).__init__(name, bases, attrs)
        if cls.type and cls.type not in MetaField.by_type:
            MetaField.by_type[cls.type] = cls
        cls.related_attrs = []
        cls.description_attrs = []
        for attr in dir(cls):
            if attr.startswith('_related_'):
                cls.related_attrs.append((attr[9:], attr))
            elif attr.startswith('_description_'):
                cls.description_attrs.append((attr[13:], attr))


class Field(object):

    __metaclass__ = MetaField
    type = None
    column_type = None  
    column_format = '%s'
    _slots = {
        'name': None,                   # name of the field
        'model_name': None,             # name of the model of this field
        'comodel_name': None,           # name of the model of values (if relational)
        '_attrs': EMPTY_DICT, 
        'store': True,                  # whether the field is stored in database
        'index': False,                 # whether the field is indexed in database
        'manual': False,                # whether the field is a custom field
        'depends': (),                  # collection of field dependencies
        'compute': None,                # compute(recs) computes field on recs
        'search': None,                 # search(recs, operator, value) searches on self
        'related': None,                # sequence of field names, for related fields
        'default': None,                # default(recs) returns the default value

        'string': None,                 # field label
        'help': None,                   # field tooltip
        'readonly': False,              # whether the field is readonly
        'required': False,              # whether the field is required
        'unique': False,                # whether the field is required
        'size': False,                # whether the field is required
    }

    def new(self, **kwargs):
        """ Return a field of the same type as ``self``, with its own parameters. """
        return type(self)(**kwargs)

    def __getattr__(self, name):
        """ Access non-slot field attribute. """
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __init__(self, string=Default, **kwargs):
        self._attrs = {}
        kwargs['string'] = string
        values = {key: val for key, val in kwargs.iteritems() if val is not Default}
        self.args = values or {}
        self.set_all_attrs(values)

    def convert_to_column(self, value, record):
        if not value:
            return None
        if isinstance(value, unicode):
            return value.encode('utf8')
        return str(value)

    def convert_to_cache(self, value, record, validate=True):
        if value is None or value is False:
            return False
        return str(value)

    def convert_to_record(self, value, record):
        return value

    def convert_to_read(self, value, record, use_name_get=True):
        return False if value is None else value

    def convert_to_write(self, value, record):
        return self.convert_to_read(value, record)

    def convert_to_export(self, value, record):
        return value or ""

    def __setattr__(self, name, value):
        try:
            object.__setattr__(self, name, value)
        except AttributeError:
            if self._attrs:
                self._attrs[name] = value
            else:
                self._attrs = {name: value}

    def set_all_attrs(self, attrs):
        assign = object.__setattr__
        for key, val in self._slots.iteritems():
            assign(self, key, attrs.pop(key, val))
        if attrs:
            assign(self, '_attrs', attrs)

    def __delattr__(self, name):
        """ Remove non-slot field attribute. """
        try:
            del self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def _setup_attrs(self, model, name):
        """ Determine field parameter attributes. """
        attrs = {}
        if not (self.args.get('automatic') or self.args.get('manual')):
            # magic and custom fields do not inherit from parent classes
            for field in reversed(resolve_mro(model, name, self._can_setup_from)):
                attrs.update(field.args)
        attrs.update(self.args)         # necessary in case self is not in class

        attrs['args'] = self.args
        attrs['model_name'] = model._name
        attrs['name'] = name

        # initialize ``self`` with ``attrs``
        if attrs.get('compute'):
            # by default, computed fields are not stored, not copied and readonly
            attrs['store'] = attrs.get('store', False)
            attrs['readonly'] = attrs.get('readonly', not attrs.get('inverse'))
        if attrs.get('related'):
            # by default, related fields are not stored and not copied
            attrs['store'] = attrs.get('store', False)
        self.set_all_attrs(attrs)

        if not self.string and not self.related:
            # related fields get their string from their parent field
            self.string = name.replace('_', ' ').capitalize()

        if self.default is not None:
            value = self.default
            self.default = value if callable(value) else lambda model: value

    @property
    def not_null(self):
        return "NOT NULL" if self.required else ""


class _String(Field):
    pass


class Char(_String):

    _slots = {"size": 6}
    type = 'char'

    def __init__(self, size=6, string=Default, **kwargs):
        super(Char, self).__init__(size=size, string=string, **kwargs)
        self.size = size

    @property
    def column_type(self):
        return 'CHAR(%d)' % self.size


class Text(_String):

    type = 'text'
    column_type = 'text'

    def __init__(self, string=Default, **kwargs):
        super(Text, self).__init__(string=string, **kwargs)


class Boolean(Field):

    type = 'boolean'
    column_type = ('int', 'int')

    def convert_to_column(self, value, record):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
            return int(bool(value))

    def convert_to_cache(self, value, record, validate=True):
        return bool(self.convert_to_column(value, record))

    def convert_to_export(self, value, record):
        value = "null" if not bool(value) else value
        return str(value)


class Integer(Field):

    type = 'integer'

    column_type = ('int', 'int')

    def convert_to_column(self, value, record):
        return int(value or 0)

    def convert_to_cache(self, value, record, validate=True):
        if isinstance(value, dict):
            return value.get('id', False)
        return int(value or 0)

    def convert_to_read(self, value, record, use_name_get=True):
        if not value:
            return int(0)
        return int(value)

    def convert_to_export(self, value, record):
        if value or value == 0:
            return str(value)


class Float(Field):

    type = 'float'

    column_type = ('real', 'real')

    def convert_to_column(self, value, record):
        return float(value or 0.00)

    def convert_to_cache(self, value, record, validate=True):
        if isinstance(value, str) and value.isdigit():
            return float(value)
        return float(value or 0)

    def convert_to_export(self, value, record):
        if value or value == 0.00:
            return str(float(value))


class Datetime(Field):

    type = 'datetime'
    column_type = ('text', 'text')

    @staticmethod
    def now(*args):
        return datetime.now().strftime(DATETIME_FORMAT)

    @staticmethod
    def from_string(value):
        if not value:
            return None
        value = value[:DATETIME_LENGTH]
        if len(value) == DATE_LENGTH:
            value += " 00:00:00"
        return datetime.strptime(value, DATETIME_FORMAT)

    @staticmethod
    def to_string(value):
        return value.strftime(DATETIME_FORMAT) if value else False

    def convert_to_cache(self, value, record, validate=True):
        if not value:
            return False
        if isinstance(value, basestring):
            if validate:
                value = self.from_string(value)
            value = value[:DATETIME_LENGTH]
            if len(value) == DATE_LENGTH:
                value += " 00:00:00"
            return value
        return self.to_string(value)

    def convert_to_column(self, value, record):
        if isinstance(value, datetime):
            value = self.to_string(value)
        return value


class Date(Field):

    type = "date"
    column_type = ('text', 'text')

    @staticmethod
    def today(*args):
        return date.today().strftime(DATE_FORMAT)

    @staticmethod
    def from_string(value):
        if not value:
            return None
        value = value[:DATE_LENGTH]
        return datetime.strptime(value, DATE_FORMAT).date()

    @staticmethod
    def to_string(value):
        return value.strftime(DATE_FORMAT) if value else False

    def convert_to_cache(self, value, record, validate=True):
        if not value:
            return False
        if isinstance(value, basestring):
            if validate:
                # force parsing for validation
                self.from_string(value)
            return value[:DATE_LENGTH]
        return self.to_string(value)

    def convert_to_column(self, value, record):
        if isinstance(value, datetime):
            value = self.to_string(value)
        return value

    def convert_to_export(self, value, record):
        if not value:
            return ''
        return self.from_string(value)


class Binary(Field):

    type = 'binary'
    column_type = ('text', 'text')

    def convert_to_column(self, value, record):
        if not isinstance(value, (str, unicode)):
            return None
        if isBase64(value):
            return value
        return encode_image(value)

    def convert_to_export(self, value, record):
        return "non-exportable"


class _Relational(Field):
    relational = True
    _slots = {
        'domain': [],
        'context': {},
    }


class Many2one(_Relational):

    type = 'many2one'
    column_type = ('int', 'int')

    def __init__(self, comodel_name=Default, string=Default, **kwargs):
        super(Many2one, self).__init__(comodel_name=comodel_name, string=string, **kwargs)

    def convert_to_record(self, value, record):
        return record.env[self.comodel_name]._browse(value)

    def convert_to_read(self, value, record, use_name_get=True):
         return value.id

    def convert_to_export(self, value, record):
        return record.env[self.comodel_name].name_get()[0][1] if value else ''
