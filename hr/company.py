from apps import base
from apps.osv import ORM, fields

class Company(ORM.BaseModel):

    _name = "company"
    _columns = {
	"code": fields.Char(string="Codigo postal", size=8, required=False),
	"reason_social": fields.Text(string="Razon social", required=False),
	"rif": fields.Text(string="Rif", required=False),
	"phone": fields.Text(string="Telefono", required=False),
	"email": fields.Text(string="Correo", required=False),
	"logo": fields.Binary(string="Logo"),
    }

Company()
