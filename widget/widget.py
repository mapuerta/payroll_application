import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class Widget(object):

    def __init__(self, widget, label, readonly=False, spacing=6):
	self.box = Gtk.Box(spacing=spacing)
	self.label = Gtk.Label(label)
	self.new_widget = widget
	self.box.pack_start(self.label, True, True, 0)
	self.box.pack_start(self.new_widget, True, True, 0)
	self.parent = None

    @property
    def widget(self):
	return self.box

    def readonly(self):
	pass

    def required(self):
	pass

    def valide(self):
	pass

    def get_value(self):
	return self.new_widget.get_value()

    def set_paren(self, new_parent):
	self.parent = new_parent
    
	
