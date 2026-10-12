import uuid
from odoo import models, fields

class SendTrackTicket(models.Model):
    _name = 'sendtrack.ticket'
    _description = 'Support Ticket'
    _order = 'create_date desc'

    name = fields.Char(string='Ticket Number', required=True, copy=False, readonly=True, default=lambda self: 'TCK-' + uuid.uuid4().hex[:8].upper())
    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description', required=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='restrict')
    shipment_id = fields.Many2one('sendtrack.shipment', string='Shipment', ondelete='set null')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium', required=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='open', required=True)

    def to_dict(self):
        self.ensure_one()
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'partner_id': self.partner_id.id,
            'partner_name': self.partner_id.name,
            'partner_email': self.partner_id.email or '',
            'shipment_id': self.shipment_id.id if self.shipment_id else None,
            'shipment_tracking_code': self.shipment_id.tracking_code if self.shipment_id else '',
            'priority': self.priority,
            'status': self.status,
            'created_at': fields.Datetime.to_string(self.create_date)
        }
