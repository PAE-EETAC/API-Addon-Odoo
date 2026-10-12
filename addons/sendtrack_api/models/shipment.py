import uuid
from odoo import models, fields, api

class SendTrackShipment(models.Model):
    _name = 'sendtrack.shipment'
    _description = 'Shipment'
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default=lambda self: 'SHP-' + uuid.uuid4().hex[:8].upper())
    tracking_code = fields.Char(string='Tracking Code', required=True, copy=False, readonly=True, default=lambda self: uuid.uuid4().hex[:12].upper())
    sender_id = fields.Many2one('res.partner', string='Sender', required=True, ondelete='restrict')
    receiver_id = fields.Many2one('res.partner', string='Receiver', required=True, ondelete='restrict')
    delivery_address = fields.Text(string='Delivery Address', required=True)
    weight = fields.Float(string='Weight (kg)', default=1.0)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)
    notes = fields.Text(string='Notes')

    def to_dict(self):
        self.ensure_one()
        return {
            'id': self.id,
            'name': self.name,
            'tracking_code': self.tracking_code,
            'sender_id': self.sender_id.id,
            'sender_name': self.sender_id.name,
            'sender_email': self.sender_id.email or '',
            'sender_phone': self.sender_id.phone or '',
            'receiver_id': self.receiver_id.id,
            'receiver_name': self.receiver_id.name,
            'receiver_email': self.receiver_id.email or '',
            'receiver_phone': self.receiver_id.phone or '',
            'delivery_address': self.delivery_address,
            'weight': self.weight,
            'status': self.status,
            'notes': self.notes or '',
            'created_at': fields.Datetime.to_string(self.create_date)
        }
