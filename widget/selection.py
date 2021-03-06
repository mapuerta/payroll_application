import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget

class Selection(Widget):

    def __init__(self, field):
	store_select = Gtk.ListStore(str, str)
	super(Selection, self).__init__(Gtk.ComboBox.new_with_model_and_entry(store_select),
				        field)
	for opt in self.selection:
	    store_select.append([opt[0], opt[1]])
	self.new_widget.set_entry_text_column(1)
					     
