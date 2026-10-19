import json
from odoo import http
from odoo.http import request
from .jwt_auth import jwt_required

class ShipmentApiController(http.Controller):

    @http.route('/api/shipments', type='http', auth='public', methods=['POST'], csrf=False)
    @jwt_required
    def create_shipment(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            payload = kwargs

        sender_id = payload.get('sender_id')
        receiver_id = payload.get('receiver_id')
        delivery_address = payload.get('delivery_address')
        weight = payload.get('weight', 1.0)
        notes = payload.get('notes', '')

        if not sender_id or not delivery_address:
            return request.make_json_response({'error': 'Fields sender_id and delivery_address are required'}, status=400)

        partner_model = request.env['res.partner'].sudo()
        sender = partner_model.browse(int(sender_id))
        if not sender.exists():
            return request.make_json_response({'error': 'Sender partner not found'}, status=404)

        if not receiver_id:
            receiver_name = payload.get('receiver_name')
            if not receiver_name:
                return request.make_json_response({'error': 'Either receiver_id or receiver_name is required'}, status=400)
            company = request.env['res.company'].sudo().search([], order='id asc', limit=1)
            company_id = company.id if company else 1
            receiver = partner_model.create({
                'name': receiver_name,
                'email': payload.get('receiver_email', ''),
                'phone': payload.get('receiver_phone', ''),
                'street': delivery_address,
                'company_id': company_id
            })
            receiver_id = receiver.id
        else:
            receiver = partner_model.browse(int(receiver_id))
            if not receiver.exists():
                return request.make_json_response({'error': 'Receiver partner not found'}, status=404)

        try:
            shipment = request.env['sendtrack.shipment'].sudo().create({
                'sender_id': int(sender_id),
                'receiver_id': int(receiver_id),
                'delivery_address': delivery_address,
                'weight': float(weight),
                'notes': notes,
                'status': 'draft'
            })
            return request.make_json_response(shipment.to_dict(), status=201)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)

    @http.route('/api/shipments/person/<int:partner_id>', type='http', auth='public', methods=['GET'], csrf=False)
    @jwt_required
    def get_shipments_by_person(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return request.make_json_response({'error': 'Partner not found'}, status=404)

        role = kwargs.get('role', 'all')
        if role == 'sender':
            domain = [('sender_id', '=', partner_id)]
        elif role == 'receiver':
            domain = [('receiver_id', '=', partner_id)]
        else:
            domain = ['|', ('sender_id', '=', partner_id), ('receiver_id', '=', partner_id)]

        try:
            shipments = request.env['sendtrack.shipment'].sudo().search(domain)
            result = [s.to_dict() for s in shipments]
            return request.make_json_response(result, status=200)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)

    @http.route('/api/shipments/track/<string:tracking_code>', type='http', auth='public', methods=['GET'], csrf=False)
    @jwt_required
    def track_shipment(self, tracking_code, **kwargs):
        shipment = request.env['sendtrack.shipment'].sudo().search([('tracking_code', '=', tracking_code)], limit=1)
        if not shipment:
            return request.make_json_response({'error': 'Shipment not found with given tracking code'}, status=404)

        return request.make_json_response(shipment.to_dict(), status=200)
