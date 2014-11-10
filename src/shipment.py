from fedex import *
from suds.client import Client
import suds
from config import FedexConfig
import os
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport.http').setLevel(logging.DEBUG)

class Shipment:

    def __init__(self):
        wsdl_path = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/wsdl/ShipService_v15.wsdl"
        self.client = Client(wsdl_path)
        
    def setConfig(self, fconfig):
        self.config = fconfig
        self.wad = createWebAuthenticationDetail(self.client, self.config.key, self.config.password)
        self.cd = createClientDetail(self.client, self.config.account_no, self.config.meter_no)
        self.td = createTransactionDetails(self.client, "International shipping using Python")
        self.version = createVersionId(self.client, 'ship', '15', '0', '0')

    def setRequestedShipment(self, dropoff_type, service_type, packing_type, shipper_contact, shipper_address,
                             recipient_contact, recipient_address, scp, ccd, label, rpli):
        rs = self.client.factory.create('RequestedShipment')
        rs.ShipTimestamp = datetime.now()
        rs.DropoffType = dropoff_type
        rs.ServiceType = service_type
        rs.PackagingType = packing_type
        rs.Shipper.Contact = shipper_contact.soap(self.client)
        rs.Shipper.Address = shipper_address.soap(self.client)
        rs.Recipient.Contact = recipient_contact.soap(self.client)
        rs.Recipient.Address = recipient_address.soap(self.client)
        rs.ShippingChargesPayment.PaymentType = addPaymentTypeValue(self.client, scp.payment_type)
        rs.ShippingChargesPayment.Payor.ResponsibleParty.AccountNumber = scp.account
        rs.ShippingChargesPayment.Payor.ResponsibleParty.Address.CountryCode = scp.country_code
        rs.CustomsClearanceDetail.DutiesPayment.PaymentType = ccd.payment_type
        rs.CustomsClearanceDetail.DutiesPayment.Payor.ResponsibleParty.AccountNumber = ccd.duty_account
        rs.CustomsClearanceDetail.DutiesPayment.Payor.ResponsibleParty.Address.CountryCode = ccd.country_code
        rs.CustomsClearanceDetail.DocumentContent = ccd.document_content
        rs.CustomsClearanceDetail.CustomsValue.Currency = ccd.customs_currency
        rs.CustomsClearanceDetail.CustomsValue.Amount = ccd.customs_amount
        rs.CustomsClearanceDetail.ExportDetail.B13AFilingOption = ccd.filing_option
        rs.CustomsClearanceDetail.Commodities = [ c.soap(self.client) for c in ccd.commodity]
        rs.LabelSpecification.LabelFormatType = label.format_type
        rs.LabelSpecification.ImageType = label.image_type
        rs.LabelSpecification.LabelStockType = label.stock_type
        rs.PackageCount = 1
        rs.RequestedPackageLineItems = [ r.soap(self.client) for r in rpli]
        self.rs = rs
        
        # 'CustomerSpecifiedDetail' => array(
	# 	'MaskedData'=> 'SHIPPER_ACCOUNT_NUMBER'
	# ), 
        
        # print rs
                
    def create_shipment(self):
        return self.client.service.processShipment(self.wad, self.cd, self.td, self.version, self.rs)

    def validate_shipment(self):
        response = self.client.service.validateShipment(WebAuthenticationDetail=self.wad,
                                                        ClientDetail=self.cd,
                                                        TransactionDetail=self.td,
                                                        Version=self.version,
                                                        RequestedShipment=self.rs)
        return response        


class LabelSpecification:

    def __init__(self, format_type, image_type, stock_type):
        self.format_type = format_type
        self.image_type = image_type
        self.stock_type = stock_type

    @property
    def dict(self):
        return { 'LabelFormatType': self.format_type,
                 'ImageType': self.image_type,
                 'Stock_Type': self.stock_type }
        
    def __repr__(self):
        return self.format_type

class Contact:

    def __init__(self, person_name, company_name, phone_no):
        self.person = person_name
        self.company = company_name
        self.phone = phone_no

    def soap(self, client):
        return addContact(client, self.person, self.company, self.phone)

class Address:

    def __init__(self, city, state_code, postal_code, country_code, street_lines):
        self.city = city
        self.state_code = state_code
        self.postal_code = postal_code
        self.country_code = country_code
        self.street_lines = street_lines

    def soap(self, client):
        return addAddress(client, self.street_lines, self.city, self.state_code,
                          self.postal_code, self.country_code)

class ShippingChargesPayment:

    def __init__(self, payment_type, bill_account_no, country_code):
        self.payment_type = payment_type
        self.account = bill_account_no
        self.country_code = country_code

    def __repr__(self):
        return self.payment_type

class CustomsClearanceDetail:

    def __init__(self, payment_type, duty_account, country_code,
                 document_content, customs_currency, customs_amount,
                 commodity, filing_option):
        self.payment_type = payment_type
        self.duty_account = duty_account
        self.country_code = country_code
        self.document_content = document_content
        self.customs_currency = customs_currency
        self.customs_amount = customs_amount
        self.commodity = commodity
        self.filing_option = filing_option

    def __repr__(self):
        return self.payment_type
        
class Commodity:

    def __init__(self, no_of_pieces, description, country_of_manufacture,
                 weight_units, weight_value, quantity, quantity_units,
                 unit_price_currency, unit_price_amount):
        self.pieces = no_of_pieces
        self.description = description
        self.country = country_of_manufacture
        self.weight_units = weight_units
        self.weight_value = weight_value
        self.quantity = quantity
        self.quantity_units = quantity_units
        self.unit_price_currency = unit_price_currency
        self.unit_price_amount = unit_price_amount
        self.customs_value_currency = unit_price_currency
        self.customs_value_amount = unit_price_amount * quantity

    def soap(self, client):
        c = client.factory.create('Commodity')
        c.NumberOfPieces = self.pieces
        c.Description = self.description
        c.CountryOfManufacture = self.country
        c.Weight.Units = self.weight_units
        c.Weight.Value = self.weight_value
        c.Quantity = self.quantity
        c.QuantityUnits = self.quantity_units
        c.UnitPrice.Currency = self.unit_price_currency
        c.UnitPrice.Amount = self.unit_price_amount
        c.CustomsValue.Currency = self.customs_value_currency
        c.CustomsValue.Amount = self.customs_value_amount
        return c

    def __repr__(self):
        return self.description

class PackageItem:

    def __init__(self, seq_no, group_pkg_no, weight_value, weight_units, dimension_length,
                 dimension_width, dimension_height, dimension_units):
        self.seq_no = seq_no
        self.group_pkg_no = group_pkg_no
        self.weight_value = weight_value
        self.weight_units = weight_units
        self.dim_length = dimension_length
        self.dim_width = dimension_width
        self.dim_height = dimension_height
        self.dim_units = dimension_units

    def soap(self, client):
        rpli = client.factory.create('RequestedPackageLineItem')
        rpli.SequenceNumber = self.seq_no
        rpli.GroupPackageCount = self.group_pkg_no
        rpli.Weight.Value = self.weight_value
        rpli.Weight.Units = self.weight_units
        rpli.Dimensions.Length = self.dim_length
        rpli.Dimensions.Width = self.dim_width
        rpli.Dimensions.Height = self.dim_height
        rpli.Dimensions.Units = self.dim_units
        return rpli

    def __repr__(self):
        return self.seq_no
        
        
if __name__ == '__main__':        
    s = Shipment()
    c = FedexConfig("fUDR24fATRGFsyBC", "gQErsywnc3obnPIpnhOIDV16X", "510087046", "118653225")
    s.setConfig(c)
    shipper_contact = Contact('Sender Name', 'Sender Company Name', '1234567890')
    shipper_address = Address('Austin', 'TX', '73301', 'US', ['Address Line 1'])
    recipient_contact = Contact('Sender Name', 'Sender Company Name', '1234567891')
    recipent_address = Address('Richmond', 'BC', 'V7C4V4', 'CA', ['Address Line 1'])
    scp = ShippingChargesPayment("SENDER", c.account_no, 'US')
    label = LabelSpecification('COMMON2D', 'PDF', 'PAPER_7X4.75')
    comm = Commodity(1, 'Books', 'US', 'LB', 1.0, 4, 'EA', 'USD', 100)
    ccd = CustomsClearanceDetail("SENDER", c.account_no, 'US', 'NON_DOCUMENTS',
                                 'USD', 100, [comm], 'NOT_REQUIRED')
    rpli = PackageItem(1, 1, 20, 'LB', 20, 20, 10, 'IN')
    s.setRequestedShipment('REGULAR_PICKUP', 'INTERNATIONAL_PRIORITY', 'YOUR_PACKAGING',
                           shipper_contact, shipper_address, recipient_contact, recipent_address,
                           scp, ccd, label, [rpli])
    try:
        re = s.validate_shipment()
    except suds.WebFault as detail:
        print detail
    #re = s.client.service.deleteShipment(1,2)
    #print re
