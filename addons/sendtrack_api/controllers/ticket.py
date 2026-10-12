import json
from odoo import http
from odoo.http import request

class TicketApiController(http.Controller):

    @http.route('/api/tickets', type='http', auth='public', methods=['POST'], csrf=False)
    def create_ticket(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            payload = kwargs

        title = payload.get('title')
        description = payload.get('description')
        partner_id = payload.get('partner_id')
        shipment_id = payload.get('shipment_id')
        tracking_code = payload.get('tracking_code')
        priority = payload.get('priority', 'medium')

        if not title or not description or not partner_id:
            return request.make_json_response({'error': 'Fields title, description and partner_id are required'}, status=400)

        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return request.make_json_response({'error': 'Partner not found'}, status=404)

        target_shipment_id = False
        if shipment_id:
            shipment = request.env['sendtrack.shipment'].sudo().browse(int(shipment_id))
            if shipment.exists():
                target_shipment_id = shipment.id
        elif tracking_code:
            shipment = request.env['sendtrack.shipment'].sudo().search([('tracking_code', '=', tracking_code)], limit=1)
            if shipment:
                target_shipment_id = shipment.id

        try:
            ticket = request.env['sendtrack.ticket'].sudo().create({
                'title': title,
                'description': description,
                'partner_id': int(partner_id),
                'shipment_id': target_shipment_id,
                'priority': priority if priority in ['low', 'medium', 'high'] else 'medium',
                'status': 'open'
            })
            return request.make_json_response(ticket.to_dict(), status=201)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)

    @http.route('/api/tickets/person/<int:partner_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_tickets_by_person(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return request.make_json_response({'error': 'Partner not found'}, status=404)

        try:
            tickets = request.env['sendtrack.ticket'].sudo().search([('partner_id', '=', int(partner_id))])
            result = [t.to_dict() for t in tickets]
            return request.make_json_response(result, status=200)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)
