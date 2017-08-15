# -*- coding: utf-8 -*-
from openerp import models, api

_DOCTYPE = {'quotation': 'sale_quotation',
            'sale_order': 'sale_order'}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        # Find doctype_id
        refer_type = _DOCTYPE.get(self._context.get('order_type'))
        doctype = self.env['res.doctype'].get_doctype(refer_type)
        fiscalyear_id = self.env['account.fiscalyear'].find()
        # --
        self = self.with_context(doctype_id=doctype.id,
                                 fiscalyear_id=fiscalyear_id)
        return super(SaleOrder, self).create(vals)
