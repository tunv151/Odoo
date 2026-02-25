# -*- coding: utf-8 -*-
import json
import logging
from odoo.http import route, Controller, request
from odoo.addons.izi_lib.helpers.Route import Route
from odoo.addons.izi_lib.helpers.ApiException import ApiException
from odoo.addons.izi_lib.helpers.Response import Response
from odoo.addons.ev_tnu_api_utils.controllers import utils
from odoo.addons.ev_config_connect_api.helpers import Configs

_logger = logging.getLogger(__name__)

api_url = Route('dot_thu', version='1', app='hp')

class HPDotThuController(Controller):

    @route(route=api_url, method=['POST'], auth='public', type='json')
    def dot_thu(self):
        try:
            verify = [
                "ma_dot_thu",
                "ma_don_vi",
                "ma_nam_hoc",
                "ma_ky_hoc",
                "ngay_dot_thu",
                "ct_ids",
            ]

            params = request.httprequest.json
            result, code, message, remote_ip, api_name, api_id = utils.check_error(
                request, api_url, require_params=verify
            )
            if result:
                raise ApiException(message=message, code=code)

            action = params.get("action")
            ma_dot_thu = params.get("ma_dot_thu")

            DotThu = request.env['hp.ql.dot.thu'].sudo()
            dot_thu = DotThu.search([('ma_dot_thu', '=', ma_dot_thu)], limit=1)

            # Validate action
            if action in ['update', 'delete'] and not dot_thu:
                return Response.error(
                    message="Mã đợt thu không tồn tại",
                    code='147'
                ).to_json()

            Configs._set_log_api(remote_ip, api_url, api_name, params, '000', 'OK')

            log_sync = request.env['log.sync.receive.dot.thu'].sudo().create({
                'params': json.dumps(params, ensure_ascii=False),
                'state': 'draft',
                'job_queue': api_id.job_queue.id,
                'ip_address': remote_ip
            })

            res = log_sync.action_handle()
            return Response.success("Thành công", data=res).to_json()

        except ApiException as e:
            return e.to_json()
