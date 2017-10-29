import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget


class Float(Widget):

    def __init__(self, field):
	super(Float, self).__init__(Gtk.SpinButton(), field)
	adjustment = Gtk.Adjustment(0.0, -2**100, 2**100, 1.0, 5.0)
	self.new_widget.set_adjustment(adjustment)
	self.new_widget.set_digits(self.digits)
	self.new_widget.set_numeric(True)
