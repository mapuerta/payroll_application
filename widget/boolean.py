import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget

class Boolean(Widget):

    def __init__(self, field):
	super(Boolean, self).__init__(Gtk.CheckButton(), field, spacing=3)
					     
