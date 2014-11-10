from fedex import *
from suds.client import Client
from config import FedexConfig
import os

class Shipment:

    def __init__(self):
        wsdl_path = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/wsdl/ShipService_v15.wsdl"
        self.client = Client(wsdl_path)
        
    def setConfig(self, fconfig):
        self.config = fconfig

if __name__ == '__main__':        
    s = Shipment()
    print s.client
    
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
