class FedexConfig:
    def __init__(self, key, password, account_no, meter_no):
        self.key = key
        self.password = password
        self.account_no = account_no
        self.meter_no = meter_no

    def __repr__(self):
        return self.key
    
