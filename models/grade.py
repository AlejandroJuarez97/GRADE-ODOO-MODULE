  # -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

# Modelo de grados (Principal) 

class Grade (models.Model):
    _name = 'res.grade'
    _description = 'Grado'

    name = fields.Char(string="Grado")
    description = fields.Text(string="Descripción")
    grade_line_ids = fields.One2many('res.grade.line', 'grade_id', string="Lista de utiles")	
    grade_inscription_ids = fields.One2many('res.grade.inscriptions', 'grade_id', string="Listado de estudiantes")

    self = fields.Many2one('res.grade', string="Grado")

# Modelo detalle (Detalle de productos)
# Listado de productos, se presenta en forma de tabla

class GradeLine (models.Model):
	_name = 'res.grade.line'
	_description = 'Lista de útiles'	
	
	product_id = fields.Many2one('product.product', string='Producto')
	grade_id = fields.Many2one('res.grade', string='Grado', require=False)
	request_qty = fields.Integer(string='Cantidad solitada', require=True)
	delivery_qyt = fields.Integer(string='Cantidad entregada', require=True)

# Modelo de inscripciones (Registro de estudiantes)
# Listado de productos, se presenta en forma de tabla

class GradeInscriptions (models.Model):
	_name = 'res.grade.inscriptions'
	_description = 'Listado de estudiantes'

	grade_id = fields.Many2one('res.grade', string="Grado")
	res_partner = fields.Many2one('res.partner', string="Estudiante")
	grade_line_ids = fields.One2many('res.grade.line', related="grade_id.grade_line_ids", string="Lista de útiles")