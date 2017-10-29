import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget


class Integer(Widget):

    def __init__(self, field):
	super(Integer, self).__init__(Gtk.SpinButton(), field)
	adjustment = Gtk.Adjustment(0, -2**100, 2**100, 1, 10, 0)
	self.new_widget.set_adjustment(adjustment)
	self.new_widget.set_numeric(True)
