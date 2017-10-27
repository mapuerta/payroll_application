from apps import base
from apps.osv import ORM, fields

class Company(ORM.BaseModel):

    _name = "company"
    _columns = {
	"code": fields.Char(string="Codigo postal", size=8, required=True),
	"reason_social": fields.Text(string="Razon social", required=True),
	"rif": fields.Text(string="Rif", required=True),
	"phone": fields.Text(string="Telefono", required=True),
	"email": fields.Text(string="Correo", required=True),
	"logo": fields.Binary(string="Logo"),
    }

Company()
