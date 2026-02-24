from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class HocPhiAPI(http.Controller):

    @http.route(
        "/api/ev/tnu/hocphi",type="json",auth="none",methods=["POST"],csrf=False,)
    def sync_hocphi(self, **kwargs):

        request_data = request.get_json_data()
        api_key = request.httprequest.headers.get("api-key")

        status = "success"
        message = ""
        response = {}

        try:
            # Check API Key
            config = request.env["ev.tnu.hocphi.api.config"].sudo().search(
                [("api_key", "=", api_key), ("active", "=", True)],
                limit=1,
            )

            if not config:
                raise Exception("Unauthorized – Invalid API Key")

            hocphi_list = request_data.get("data", [])

            for item in hocphi_list:
                code = item.get("code")

                if not code:
                    continue

                record = request.env["tnu.hocphi.category"].sudo().search(
                    [("code", "=", code)],
                    limit=1,
                )

                vals = {
                    "code": code,
                    "name": item.get("name"),
                    "amount": item.get("amount"),
                    "academic_year": item.get("academic_year"),
                }

                if record:
                    record.write(vals)
                else:
                    request.env["tnu.hocphi.category"].sudo().create(vals)

            message = "Sync học phí thành công"

            response = {
                "success": True,
                "message": message,
            }

        except Exception as e:
            status = "error"
            message = str(e)

            _logger.error("HocPhi API Error: %s", message)

            response = {
                "success": False,
                "error": message,
            }

        # Log
        request.env["ev.tnu.log.sync.receive.hocphi"].sudo().create({
            "request_data": json.dumps(request_data, ensure_ascii=False),
            "response_data": json.dumps(response, ensure_ascii=False),
            "status": status,
            "message": message,
        })

        return response
