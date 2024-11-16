# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Repairs(models.Model):
    _inherit = 'repair.order'

    installation_date = fields.Date(string= "Installation Date")
    failure_date= fields.Date(string="Failure Date")
    time_to_failure= fields.Float(string="Time To Failure (Months)", compute='_number_of_months', store= True)
    marca = fields.Char(string="marca")
    modelo = fields.Char(string="modelo")
    cor = fields.Char(string="cor")
    acessorio = fields.Char(string="acessorio")
    serial_number =fields.Char(string="Serial Number")
    defeito = fields.Char(string="defeito")
    production_batch=fields.Char(string="Production Lot", compute='_production_batch_failure', store= True)

    @api.depends("failure_date","installation_date")

    def _number_of_months(self):
        for session in self:
            if session.installation_date and session.failure_date:
                # Parse the dates into datetime objects
                installation_date_obj = fields.Date.from_string(session.installation_date)
                failure_date_obj = fields.Date.from_string(session.failure_date)

                # Calculate the difference between the two dates
                delta = failure_date_obj - installation_date_obj

                # Get the number of months in the difference
                months = delta.days / 30

                session.time_to_failure = months
            else:
                session.time_to_failure = 0.0

    @api.depends("serial_number")
    def _production_batch_failure(self):
        for session in self:
            if session.serial_number:
                # Take the first 3 letters of the serial number as the production batch
                session.production_batch = session.serial_number[:3]
            else:
                session.production_batch = ''


