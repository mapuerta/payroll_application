import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class Widget(object):

    _slots = {
	"readonly": False,
	"required": False,
	"comodel_name": False,
	"String": False,
	"selection": [],
	"digits": 0,
	"size": 10,
    }

    def __init__(self, widget, field, spacing=3):
	self.set_all_attrs(field)
	self.box = Gtk.Box(spacing=spacing)
	self.label = Gtk.Label(self.String)
	self.new_widget = widget
	self.box.pack_start(self.label, True, True, 0)
	self.box.pack_start(self.new_widget, True, True, 0)
	self.parent = None
	self._model = None
	self.set_readonly()

    def set_all_attrs(self, field):
	for key, value in self._slots.items():
	    if hasattr(field, key):
		value = getattr(field, key)
	    setattr(self, key, value)

    @property
    def widget(self):
	return self.box

    def set_readonly(self):
	if self.readonly:
	    self._readonly()

    def validate_required(self):
	if self.required:
	    self._required()

    def validate_format(self):
	return True

    def all_validate(self):
	self.validate_required()
	sef.validate_format()

    def on_save(self):
	self.all_validate()
	return self.get_value()

    def set_paren(self, new_parent):
	self.parent = new_parent

    def set_expander(self):
	self.box.set_homogeneous(False)

    def set_model(self, model):
	self._model = model

    def get_value(self):
	return self.new_widget.get_text()
	
    
	
