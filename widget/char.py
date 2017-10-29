import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget


class Char(Widget):
    def __init__(self, field, **kwargs):
	super(Char, self).__init__(Gtk.Entry(), field)
	self.new_widget.set_max_length(self.size)

    def get_value(self):
	return self.new_widget.get_text()
