from odoo import api,fields,models,_
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit ='purchase.order'

    # Define function to split purchase ordeline when we click on button
    def btn_split_rfq(self):
        for record in self:
            if record.order_line:
                cnt = 0
                for rec in record.order_line:
                    if rec.split and rec.split_qty == 0 or rec.split_qty > rec.product_qty:
                        raise ValidationError(_('Split QTY must be higher than zero and less than or equal Quantity.'))
                    if rec.split:
                        cnt += 1
                if cnt >= 1:
                    quotation_id = self.copy()
                    if quotation_id:
                        for line in quotation_id.order_line:
                            if not line.split:
                                line.unlink()
                            else:
                                line.write({
                                    'product_qty': line.split_qty,
                                    'split_qty': 0.0,
                                    'split': False
                                })
                    for order_line in record.order_line:
                        if order_line.split:
                            product_qty = order_line.product_qty - order_line.split_qty
                            order_line.write({
                                'product_qty': product_qty,
                                'split_qty': 0.0,
                                'split': False
                            })
                        if order_line.product_qty == 0.0:
                            self.env['purchase.order.line'].browse(order_line.id).unlink()
                else:
                    raise ValidationError(_('Please Select Order Line To Split'))
