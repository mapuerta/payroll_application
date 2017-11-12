import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from widget import Widget
import datetime

class DialogTime(Gtk.Dialog):

    def __init__(self, parent, last_value, label="Tiempo", calendar=False):
        Gtk.Dialog.__init__(self, label, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
	self.last_value = last_value
	adjustment = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
	self.interval = [("Hora", "hour"), ("Minutos", "min"), ("Segundos", "second")]
	self.hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
	self.box = self.get_content_area()
	self.box.set_orientation(Gtk.Orientation.VERTICAL)
	for title, val in self.interval:
	    setattr(self, val, Gtk.SpinButton())
	    getattr(self, val).set_numeric(True)
	    getattr(self, val).set_adjustment(Gtk.Adjustment(0, 0, 60, 1, 10, 0))
	    self.set_last_time(val)
	    self.hbox.add(Gtk.Label(title))
	    self.hbox.add(getattr(self, val))
	if calendar:
	    self.box.pack_start(calendar, True, False, 0)
	self.box.add(self.hbox)
        self.set_default_size(250, 200)
        self.show_all()

    def time_to_string(self):
	hour = self.hour.get_value_as_int()
	minutes = self.min.get_value_as_int()
	seconds = self.second.get_value_as_int()
	time = datetime.time(hour, minutes, seconds)
   	return time.strftime("%H:%M:%S")
   	
    def get_value(self):
	return self.time_to_string()

    def set_last_time(self, value, data=False):
	value_time = dict((i[1], 0) for i in self.interval)
	last_value = self.last_value
	if data:
	    last_value = data
	if last_value == "00:00:00":
	    return True
	hour, min, second = last_value.split(":")
	value_time["hour"] = hour
	value_time["min"] = min
	value_time["second"] = second
	getattr(self, value).set_value(int(value_time[value]))

class Time(Widget):

    def __init__(self, field):
	super(Time, self).__init__(Gtk.Entry(), field)
	self.new_widget.set_text("00:00:00")
	self.new_widget.set_editable(False)
	icon_name = Gtk.STOCK_CDROM
	self.new_widget.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
	self.new_widget.connect("icon-press", self.on_open_menu)
	
        
    def on_open_menu(self, *args):
	last_value = self.new_widget.get_text()
	dialog = DialogTime(self.parent, last_value)
        response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    self.new_widget.set_text(dialog.get_value())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
             dialog.destroy()


class DialogDateTime(DialogTime):

    def __init__(self, parent, last_value):
	self.calendar = Gtk.Calendar()
	super(DialogDateTime, self).__init__(parent, last_value,
	                                     label="Fecha y Hora",
					     calendar=self.calendar)
	self.hbox.set_orientation(Gtk.Orientation.HORIZONTAL)

    def set_last_time(self, value):
	if not self.last_value:
	    return
	date, time = self.last_value.split(" ")
	day, moth, year = date.split("-")
	self.calendar.select_day(int(day))
	self.calendar.select_month(int(moth), int(year))
	return super(DialogDateTime, self).set_last_time(value, data=time)

    def date_to_string(self):
	year, month, day = self.calendar.get_date()
	date = datetime.datetime(year, month+1, day)
   	return date.strftime("%d-%m-%Y")

    def get_value(self):
	date = "{0} {1}".format(self.date_to_string(), self.time_to_string())
	return date


class Datetime(Widget):

    def __init__(self, field):
	super(Datetime, self).__init__(Gtk.Entry(), field)
	icon_name = Gtk.STOCK_CDROM
	self.new_widget.set_editable(False)
	self.new_widget.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,
            icon_name)
	self.new_widget.connect("icon-press", self.on_open_menu)

    def on_open_menu(self, *args):
	last_value = self.new_widget.get_text()
	dialog = DialogDateTime(self.parent, last_value)
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
	    self.new_widget.set_text(dialog.get_value())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
             dialog.destroy()

    def get_value(self):
	return self.new_widget.get_text()
