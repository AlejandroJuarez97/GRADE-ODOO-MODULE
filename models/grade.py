# -*- coding: utf-8 -*-
from openerp.tools.translate import _ 
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

# Modelo de grados (Principal) 
class Grade (models.Model):
    _name = 'res.grade'
    _description = 'Grado'

    name = fields.Char(string="Grado")
    description = fields.Text(string="Descripción")
    grade_line_ids = fields.One2many('res.grade.line', 'grade_id', string="Lista de utiles")
    grade_inscription_ids = fields.One2many('res.grade.inscriptions', 'grade_id', string="Listado de estudiantes")

# Modelo detalle (Detalle de productos)
# Listado de productos, se presenta en forma de tabla
class GradeLine (models.Model):
	_name = 'res.grade.line'
	_description = 'Lista de utiles'	
	
	product_id = fields.Many2one('product.product', string='Producto', delagate=True)
	grade_id = fields.Many2one('res.grade', string='Grado', require=False)
	request_qty = fields.Integer(string='Cantidad solitada', require=True)
	#delivery_qyt = fields.Integer(string='Cantidad entregada', require=True)

# Modelo de inscripciones (Registro de estudiantes)
# Listado de productos, se presenta en forma de tabla
class GradeInscriptions (models.Model):
	_name = 'res.grade.inscriptions'
	_description = 'Listado de estudiantes'

	grade_id = fields.Many2one('res.grade', string="Grado")
	res_partner = fields.Many2one('res.partner', string="Estudiante")
	grade_line_ids = fields.One2many('res.grade.util.list', 'res_partner_id', string="Listado de útiles", compute="_set_grade_util_list")

	@api.one
	def _set_grade_util_list (self):
		records = self.env['res.grade.util.list'].search([('res_partner_id', '=', self.res_partner.id)])
		self.grade_line_ids = records

	@api.model
	def create (self, values):
		model = super(GradeInscriptions, self).create(values)
		g_lines = self.env['res.grade.line'].search([('grade_id', '=', values['grade_id'])])
		records = []

		for x in g_lines:
			vals = self.env['res.grade.util.list'].create({
				'product': x['product_id'].name,
				'request_qty': x['request_qty'],
				'delivery_qyt': 0,
				'res_partner_id': values['res_partner']
			})

			records.append(vals.id)

		values['grade_line_ids'] = records
		return model

	@api.model
	def unlink (self):
		records = self.env['res.grade.util.list'].search([('res_partner_id', '=', self.res_partner.id)]).unlink()
		return super(GradeInscriptions, self).unlink()

	@api.multi
	def action_view_grade_inscription_line (self):
	    view = self.env.ref('grade.grade_util_list_view')

	    return {
	        'type': 'ir.actions.act_window',
	        'view_type': 'form',
	        'view_mode': 'form',
	        'res_model': self._name,
	        'views': [(view.id, 'form')],
	        'view_id': view.id,
	        'res_id': self.id,
	        'context': self.env.context
	    }


# Modelo de inscripciones (Registro de utiles por estudiantes)
# Listado de productos por estudiante, se presenta en forma de tabla

class GradeUtilList(models.Model):
	_name = 'res.grade.util.list'
	_description = 'Lista de útiles'

	product = fields.Text(string="Producto", readonly=True)
	res_partner_id = fields.Many2one('res.partner', string="Estudiante", readonly=True)
	request_qty = fields.Integer(string='Cantidad solitada', require=True, readonly=True)
	delivery_qyt = fields.Integer(string='Cantidad entregada', require=True)
