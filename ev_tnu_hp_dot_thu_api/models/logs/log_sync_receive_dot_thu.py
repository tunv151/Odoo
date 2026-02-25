# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from odoo import models, fields

_logger = logging.getLogger(__name__)

class LogSyncReceiveDotThu(models.Model):
    _name = 'log.sync.receive.dot.thu'
    _inherit = 'log.sync.receive'
    _description = 'Log nhận đồng bộ đợt thu'
    _rec_name = 'code'

    dot_thu_id = fields.Many2one('hp.ql.dot.thu')

    def action_handle(self):
        try:
            params = json.loads(self.params or "{}")

            action = params.get('action')
            ma_dot_thu = params.get('ma_dot_thu')

            DotThu = self.env['hp.ql.dot.thu'].sudo()
            SinhVienLine = self.env['hp.dot.thu.sinh.vien'].sudo()
            ChiTietLine = self.env['hp.dot.thu.sinh.vien.chi.tiet'].sudo()
            Partner = self.env['res.partner'].sudo()
            Product = self.env['product.template'].sudo()

            dot_thu = DotThu.search([('ma_dot_thu', '=', ma_dot_thu)], limit=1)

            # DELETE
            if action == 'delete':
                if dot_thu:
                    dot_thu.write({'active': False})
                self.write({
                    'state': 'done',
                    'date_done': datetime.now()
                })
                return '000'

            # VALIDATE FK
            business_unit = self.env['res.business.unit'].sudo().search(
                [('code', '=', params.get('ma_don_vi'))], limit=1)

            nam_hoc = self.env['hp.nam.hoc'].sudo().search(
                [('ma_nam_hoc', '=', params.get('ma_nam_hoc'))], limit=1)

            ky_hoc = self.env['hp.ky.hoc'].sudo().search(
                [('ma_ky_hoc', '=', params.get('ma_ky_hoc'))], limit=1)

            if not business_unit or not nam_hoc or not ky_hoc:
                self.write({'state': 'fail', 'date_done': datetime.now()})
                return '147'

            vals = {
                'ma_dot_thu': ma_dot_thu,
                'business_unit_id': business_unit.id,
                'nam_hoc_id': nam_hoc.id,
                'ky_hoc_id': ky_hoc.id,
                'ngay_dot_thu': params.get('ngay_dot_thu'),
                'mo_ta': params.get('mo_ta'),
                'active': True,
            }

            if dot_thu:
                dot_thu.write(vals)
                dot_thu.line_ids.unlink()
            else:
                dot_thu = DotThu.create(vals)

            # XỬ LÝ CHI TIẾT
            ct_ids = params.get('ct_ids') or {}

            for ma_sv, khoan_list in ct_ids.items():
                partner = Partner.search([('ma_sinh_vien', '=', ma_sv)], limit=1)
                if not partner:
                    continue

                sv_line = SinhVienLine.create({
                    'dot_thu_id': dot_thu.id,
                    'partner_id': partner.id,
                })

                for item in khoan_list:
                    product = Product.search(
                        [('default_code', '=', item.get('ma_khoan_thu'))],
                        limit=1
                    )
                    if not product:
                        continue

                    ChiTietLine.create({
                        'sinh_vien_line_id': sv_line.id,
                        'product_id': product.id,
                        'so_tien': item.get('so_tien')
                    })

            self.write({
                'dot_thu_id': dot_thu.id,
                'state': 'done',
                'date_done': datetime.now()
            })

            return '000'

        except Exception as e:
            _logger.error(e)
            self.write({
                'state': 'fail',
                'date_done': datetime.now()
            })
            return '096'
