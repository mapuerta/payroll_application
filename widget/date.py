import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget
import datetime

class DialogCalendar(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Calendario", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
	self.calendar = Gtk.Calendar()
        self.set_default_size(250, 200)
        box = self.get_content_area()
        box.add(self.calendar)
        self.show_all()

    def date_to_string(self):
	year, month, day = self.calendar.get_date()
	date = datetime.datetime(year, month+1, day)
   	return date.strftime("%d-%m-%Y")
   	
    def get_value(self):
	return self.date_to_string()
	

class Date(Widget):

    def __init__(self, field):
	super(Date, self).__init__(Gtk.Entry(), field)
	icon_name = Gtk.STOCK_CDROM
	self.new_widget.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
	self.new_widget.connect("icon-press", self.on_open_menu)
        
    def on_open_menu(self, *args):
	dialog = DialogCalendar(self.parent)
        response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    self.new_widget.set_text(dialog.get_value())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
             dialog.destroy()

    def get_value():
	return self.new_widget.get_text()

    def validate_format(self):
	try:
	    datetime.datetime.strptime(self.new_widget.get_text(), '%Y-%m-%d')
	except ValueError:
	    raise ValueError("Incorrect data format, should be YYYY-MM-DD")

