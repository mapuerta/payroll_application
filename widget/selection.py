import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget

class Selection(Widget):

    def __init__(self, field):
	label = field.String
	select_opt = field.Selection
	store_select = Gtk.ListStore(str, str)
	for opt in select_opt:
	    store_select.append([opt[0], opt[1]])
	super(Selection, self).__init__(Gtk.ComboBox.new_with_model_and_entry(store_select),
				        label, spacing=6, readonly=False)
	self.new_widget.set_entry_text_column(1)
					     
