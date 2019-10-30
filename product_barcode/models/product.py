# -*- coding: utf-8 -*-
from odoo import api, fields, models
import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    mfd = fields.Char(compute='_compute_mrp_mfd', string='Manufacturing Date')

    def _compute_mrp_mfd(self):
        for template in self:
            template.mfd = template.mapped('product_variant_ids').mapped('mfd')[0] or ''

class ProductProduct(models.Model):
    _inherit = 'product.product'

    mfd = fields.Char(compute='_compute_mrp_mfd', string='Manufacturing Date')

    def _compute_mrp_mfd(self):
        domain = [('state', '=', 'done'), ('product_id', 'in', self.ids)]
        mos = self.env['mrp.production'].search(domain)
        for product in self:
            product_mos = mos.filtered(lambda x: x.product_id.id == product.id).sorted(key='id', reverse=True)
            finished_date = product_mos and product_mos.mapped('date_finished')[0] or ''
            product.mfd = finished_date and (finished_date.strftime("%b %Y")) or ''
