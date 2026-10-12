import json
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

class AuthApiController(http.Controller):

    @http.route('/api/auth/login', type='http', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            payload = kwargs

        login = payload.get('login') or payload.get('email')
        password = payload.get('password')

        if not login or not password:
            return request.make_json_response({'error': 'Fields email and password are required'}, status=400)

        try:
            credential = {'login': login, 'password': password, 'type': 'password'}
            auth_info = request.session.authenticate(request.env, credential)
            uid = auth_info.get('uid') or request.session.uid
            if not uid:
                return request.make_json_response({'error': 'Invalid credentials'}, status=401)

            user = request.env['res.users'].sudo().browse(uid)
            partner = user.partner_id

            response_data = {
                'session_id': request.session.sid,
                'user_id': user.id,
                'partner_id': partner.id,
                'name': user.name,
                'email': user.email or '',
                'phone': partner.phone or '',
                'street': partner.street or ''
            }
            return request.make_json_response(response_data, status=200)
        except AccessDenied:
            return request.make_json_response({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)

    @http.route('/api/auth/logout', type='http', auth='public', methods=['POST'], csrf=False)
    def logout(self, **kwargs):
        try:
            request.session.logout()
            return request.make_json_response({'status': 'logged_out'}, status=200)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)

    @http.route('/api/auth/register', type='http', auth='public', methods=['POST'], csrf=False)
    def register(self, **kwargs):
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            payload = kwargs

        name = payload.get('name')
        email = payload.get('email')
        password = payload.get('password')
        phone = payload.get('phone', '')
        street = payload.get('street', '')

        if not name or not email or not password:
            return request.make_json_response({'error': 'Fields name, email and password are required'}, status=400)

        existing_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        if existing_user:
            return request.make_json_response({'error': 'User with this email already exists'}, status=409)

        try:
            company = request.env['res.company'].sudo().search([], order='id asc', limit=1)
            company_id = company.id if company else 1

            user = request.env['res.users'].sudo().with_company(company_id).create({
                'name': name,
                'login': email,
                'email': email,
                'password': password,
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
            })

            partner = user.partner_id
            partner.sudo().write({
                'phone': phone,
                'street': street,
                'company_id': company_id,
            })

            response_data = {
                'user_id': user.id,
                'partner_id': partner.id,
                'name': user.name,
                'email': user.email,
                'phone': phone,
                'street': street
            }
            return request.make_json_response(response_data, status=201)
        except Exception as e:
            return request.make_json_response({'error': str(e)}, status=500)
