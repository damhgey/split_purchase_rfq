from odoo import api, fields, models, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    split = fields.Boolean(string='Split')
    split_qty = fields.Float(string="Split QTY")
