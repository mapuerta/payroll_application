import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from date import Date
from many2one import Related
from selection import Selection
from form import Form

class Fieldtest(object):
    def __init__(self, String, Selection=[("M", "Masculino"), ("F", "Femenino")]):
	self.String = String
	self.Selection = Selection

view = Form(False, "test")

for i in range(1):
    view.new_witget( Related(Fieldtest("Empleados"), None))
for i in range(1):
    view.new_witget(Date(Fieldtest("Fecha")))
for i in range(12):
    view.new_witget(Selection(Fieldtest("Genero")))
#~ view.new_witget(field2)
view.show_all()
Gtk.main()

