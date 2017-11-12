import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from date import Date
from calendar import Time, Datetime
from many2one import Related
from selection import Selection
from boolean import Boolean
from integer import Integer
from float import Float
from text import Text
from char import Char
from form import Form

class Fieldtest(object):
    def __init__(self, String, selection=[("M", "Masculino"), ("F", "Femenino")],
		 digits=2, comodel_name="model", size=5, required=False):
	self.String = String
	self.selection = selection
	self.digits = digits
	self.comodel_name = comodel_name
	self.size = size
	self.required = required

view = Form(False, "test")

for i in range(1):
    view.new_witget(Related(Fieldtest("Empleados")))
    #~ view.new_witget(Date(Fieldtest("Fecha")))
    #~ view.new_witget(Selection(Fieldtest("Genero")))
    #~ view.new_witget(Boolean(Fieldtest("Fijo")))
    #~ view.new_witget(Integer(Fieldtest("Capital")))
    #~ view.new_witget(Float(Fieldtest("Sueldo")))
    #~ view.new_witget(Time(Fieldtest("Time")))
    #~ view.new_witget(Text(Fieldtest("Nota"), **{"widget":"textbox"}))
    view.new_witget(Char(Fieldtest("Codigo", required=True)))
    view.new_witget(Datetime(Fieldtest("Entrada")))
view.show_all()
Gtk.main()

