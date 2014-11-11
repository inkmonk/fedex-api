from suds.client import Client
from datetime import datetime

def createWebAuthenticationCredential(client, key, password):
    wac = client.factory.create('WebAuthenticationCredential')
    wac.Key = key
    wac.Password = password
    return wac

def createWebAuthenticationDetail(client, key, password):
    wad = client.factory.create('WebAuthenticationDetail')
    wad.UserCredential = createWebAuthenticationCredential(client, key, password)
    return wad

def createClientDetail(client, account_no, meter_no):
    cd = client.factory.create('ClientDetail')
    cd.AccountNumber = account_no
    cd.MeterNumber = meter_no
    return cd

def createTransactionDetails(client, transaction_id):
    td = client.factory.create('TransactionDetail')
    td.CustomerTransactionId = transaction_id
    return td

def createVersionId(client, service_id, major, intermediate, minor):
    ver = client.factory.create('VersionId')
    ver.ServiceId = service_id
    ver.Major = major
    ver.Intermediate = intermediate
    ver.Minor = minor
    return ver

def addContact(client, pname, c_name, phone_no):
    contact = client.factory.create('Contact')
    contact.PersonName = pname
    contact.CompanyName = c_name
    contact.PhoneNumber = phone_no
    return contact

def addAddress(client, street_lines = None, city = None,
               state_code=None, postal_code=None, country_code=None):
    """
    street_lines: Type list of string
    """
    address = client.factory.create('Address')
    address.City = city
    address.StreetLines = street_lines
    address.StateOrProvinceCode = state_code
    address.PostalCode = postal_code
    address.CountryCode = country_code
    return address
    
def addShipper(client, pname, c_name, phone_no, street_lines, city,
               state_code, postal_code, country_code):
    shipper = client.factory.create('Party')
    shipper.Contact = addContact(client, pname, c_name, phone_no)
    shipper.Address = addAddress(client, street_lines, city,
                                 state_code, postal_code, country_code)
    return shipper

def addShippingChargesPayment(client, bill_account_no, payment_type, country_code):
    scp = client.factory.create('Payment')
    ptype = client.factory.create('PaymentType')
    if payment_type == "SENDER":
        scp.PaymentType = ptype.SENDER
    party = client.factory.create('Party')
    party.AccountNumber = bill_account_no
    address = client.factory.create('Address')
    address.CountryCode = country_code
    party.Address = address
    payor = client.factory.create('Payor')
    payor.ResponsibleParty = party
    scp.Payor = payor
    return scp

def addWeight(client, units, value):
    weight = client.factory.create('Weight')
    weight.Units = units
    weight.Value = value
    return weight

def commodity(no_of_pieces, description, country, units, value, quantity,
              quantity_units, currency, amount):
    return {'NumberOfPieces': no_of_pieces, 'Description': description,
            'CountryOfManufacture': country, 'Weight': {'Units':units, 'Value': value},
            'Quantity':quantity, 'QuantityUnits': quantity_units,
            'UnitPrice': {'Currency': currency, 'Amount': amount},
            'CustomsValue': {'Currency': currency, 'amount': quantity * amount}}

def addMoney(client, currency, amount):
    money = client.factory.create('Money')
    money.Currency = currency
    money.Amount = amount
    return money

def addExportDetail(client, filing_option):
    ed = client.factory.create('ExportDetail')
    fo = client.factory.create('B13AFilingOptionType')
    if filing_option == "NOT_REQUIRED":
        ed.B13AFilingOption = fo.NOT_REQUIRED
    return ed

def addDocumentContentValue(client, content):
    dc = client.factory.create('InternationalDocumentContentType')
    if content == "NON_DOCUMENTS":
        return dc.NON_DOCUMENTS
    raise Exception("Should not reach here")

def addPaymentTypeValue(client, payment_type):
    pt = client.factory.create('PaymentType')
    if payment_type == "SENDER":
        return pt.SENDER
    raise Exception("Should not reach here")

def addParty(client, duty_account):
    party = client.factory.create('Party')
    party.AccountNumber = duty_account
    
        
def addPayor(client, duty_account, country_code):
    payor = client.factory.create('Payor')
    payor.ResponsibleParty = addParty(client, duty_account)
    payor.Address = addAddress(client, country_code=country_code)
    return payor
    
    
        
def addPayment(client, payment_type, duty_account, country_code):
    payment = client.factory.create('Payment')
    payment.PaymentType = addPaymentTypeValue(client, payment_type)
    payment.Payor = addPayor(client, duty_account, country_code)
    return payment
        
def addCustomerClearanceDetail(client, doc_value, cus_currency, cus_amount, commodities,
                               payment_type, duty_account, country_code, filing_option):
    ccd = client.factory.create('CustomsClearanceDetail')
    ccd.DutiesPayment = addPayment(client, payment_type, duty_account, country_code)
    ccd.DocumentContent = addDocumentContentValue(client, doc_value)
    ccd.CustomsValue = addMoney(client, cus_currency, cus_amount)
    ccd.Commodities = commodities
    ccd.ExportDetail = addExportDetail(client, filing_option)
    return ccd

def addDropoffValue(client, value):
    dv = client.factory.create('DropoffType')
    if value == "BUSINESS_SERVICE_CENTER":
        return dv.BUSINESS_SERVICE_CENTER
    if value == "DROP_BOX":
        return dv.DROP_BOX
    if value == "REGULAR_PICKUP":
        return dv.REGULAR_PICKUP
    if value == "REQUEST_COURIER":
        return dv.REQUEST_COURIER
    if value == "STATION":
        return dv.STATION
    raise Exception("Should not reach here")

def addServiceValue(client, value):
    s = client.factory.create('ServiceType')
    if value == "INTERNATIONAL_PRIORITY":
        return s.INTERNATIONAL_PRIORITY
    raise Exception("Should not reach here")

def addPackingValue(client, value):
    p = client.factory.create('PackagingType')
    if value == "YOUR_PACKAGING":
        return p.YOUR_PACKAGING
    raise Exception("Should not reach here")

def addFilingValue(client, value):
    fv = client.factory.create('B13AFilingOptionType')
    if value == 'NOT_REQUIRED':
        return fv.NOT_REQUIRED
    raise Exception("Should not reach here")

def addLabelFormatValue(client, value):
    lf = client.factory.create('LabelFormatType')
    if value == "COMMON2D":
        return lf.COMMON2D
    raise Exception("Should not reach here")

def addShippingImageType(client, value):
    si = client.factory.create('ShippingDocumentImageType')
    if value == "PDF":
        return si.PDF
    raise Exception("Should not reach here")

def addLabelStockValue(client, value):
    ls = client.factory.create('LabelStockType')
    if value == 'PAPER_4X6':
        return ls.PAPER_4X6
    raise Exception("Should not reach here")
        
    
# def addRequestedShipment(client, client, pname, c_name, phone_no, street_lines, city,
#                          state_code, postal_code, country_code, bill_account_no,
#                          payment_type):
#     rs = client.factory.create('RequestedShipment')
#     rs.ShipTimestamp = datetime.now()
#     rs.DropoffType = drop_off_type
#     rs.ServiceType = service_type
#     rs.PackagingType = package_type
#     rs.Shipper = addShipper(client, client, pname, c_name, phone_no, street_lines, city,
#                             state_code, postal_code, country_code)
#     #rs.Recipient = addRecipient()
#     rs.ShippingChargesPayment = addShippingChargesPayment(client, bill_account_no,
#                                                           payment_type, country_code)
#     rs.CustomsClearanceDetail = addCustomerClearanceDetail(client, doc_value, cus_currency, cus_amount, commodities,
#                                                            payment_type)
# client = Client('file:///home/dev/github/fedex-api/src/wsdl/ShipService_v15.wsdl')
