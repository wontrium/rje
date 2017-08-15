# -*- coding: utf-8 -*-
from openerp import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _switch_move_dict_dr_cr(self, move_dict):
        move_lines = []
        for line_dict in move_dict['line_id']:
            line_dict[2].update({'credit': line_dict[2]['debit'],
                                 'debit': line_dict[2]['credit'],
                                 })
            move_lines.append((0, 0, line_dict[2]))
        return move_dict

    @api.multi
    def _switch_dr_cr(self):
        self.ensure_one()
        if self.state == 'posted':
            self.button_cancel()
        for line in self.line_id:
            line.write({'credit': line.debit, 'debit': line.credit})
        self.button_validate()

    @api.model
    def _reconcile_voided_entry(self, move_ids):
        AccountMoveLine = self.env['account.move.line']
        # Getting move_line_ids of the voided documents.
        move_lines = \
            AccountMoveLine.search([('account_id.reconcile', '=', True),
                                    ('reconcile_id', '=', False),
                                    ('move_id', 'in', move_ids)])
        if move_lines:
            move_lines.reconcile('manual')

    @api.model
    def _reconcile_voided_entry_by_account(self, move_ids, account_id):
        AccountMoveLine = self.env['account.move.line']
        # Getting move_line_ids of the voided documents.
        move_lines = \
            AccountMoveLine.search([('account_id.reconcile', '=', True),
                                    ('reconcile_id', '=', False),
                                    ('move_id', 'in', move_ids),
                                    ('account_id', '=', account_id)])
        if move_lines:
            move_lines.reconcile('manual')
