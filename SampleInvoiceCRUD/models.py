from __future__ import unicode_literals
from django.db import models
import json

# Class that ignores class attributes with value as None
class _State:
    def __getstate__(self):
        state = self.__dict__.copy()
        state = {key: value for key, value in state.items() if value is not None}
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

class Invoice(_State):
    def __init__(self, CustomerName=None, CustomerId=None, TxnDate=None):
        self.Line = []
        self.CustomerRef = None

        self.Id = None
        self.CustomField = None
        self.DocNumber = None
        self.TxnDate = None
        self.DepartmentRef = None
        self.PrivateNote = None
        self.LinkedTxn = None
        self.TxnTaxDetail = None
        
        self.CustomerMemo = None
        self.BillAddr = None
        self.ShipAddr = None
        self.ClassRef = None
        self.SalesTermRef = None
        self.DueDate = None
        self.GlobalTaxCalculation = "TaxExcluded"
        self.ShipMethodRef = None
        self.ShipDate = None
        self.TrackingNum = None
        self.TotalAmt = None
        self.CurrencyRef = None
        self.ExchangeRate = 1
        
        self.ApplyTaxAfterDiscount = False
        self.PrintStatus = "NotSet"
        self.EmailStatus = "NotSet"
        self.BillEmail = None
        self.BillEmailCc = None
        self.BillEmailBcc = None
        self.DeliveryInfo = None
        self.Balance = None
        self.TxnSource = None
        self.Deposit = None
        self.MetaData = None
        self.HomeTotalAmt = None
        self.HomeBalance = None

        # for update
        self.sparse = None
        self.SyncToken = None

    def printInvoice(self):
        print(self.Id+' '+self.DocNumber+' '+self.TxnDate)

# Helper classes
class LineItem(_State):
    lineTypeDict = {
        "DescriptionOnly": "DescriptionLineDetail"
    }
    def __init__(self, LineType, Amount, Id=None, LineNum=None, Description=None):
        self.Id = Id
        self.LineNum = LineNum
        self.Description = Description
        self.DetailType = LineType
        self.Amount = Amount
        if LineType == "SalesItemLineDetail":
            setattr(self, LineType, None)
        elif LineType == "DescriptionOnly":
            setattr(self, LineTypeDict[LineType], None)
        elif LineType == "DiscountLineDetail":
            setattr(self, LineType, None)
        elif LineType == "SubtotalLineDetail":
            setattr(self, LineType, None)

class SalesLineItem(_State):
    def __init__(self):
        self.ItemRef = None
        self.ClassRef = None
        self.UnitPrice = None
        self.MarkupInfo = None
        self.Qty = None
        self.ItemAccountRef = None
        self.TaxCodeRef = None
        self.ServiceDate = None
        self.TaxInclusiveAmt = None

class DescriptionLineItem(_State):
    def __init__(self):
        self.ServiceDate = None
        self.TaxCodeRef = None

class DiscountLineItem(_State):
    def __init__(self):
        self.PercentBased = None
        self.DiscountPercent = None
        self.DiscountAccountRef = None
        self.ClassRef = None
        self.TaxCodeRef = None

class SubtotalLineItem(_State):
    def __init__(self):
        self.ItemRef = None

class TaxLineItem(_State):
    def __init__(self):
        self.PercentBased = None
        self.NetAmountTaxable = None
        self.TaxInclusiveAmount = None
        self.OverrideDeltaAmount = None
        self.TaxPercent = None
        self.TaxRateRef = None

class Ref(_State):
    def __init__(self, value=None, name=None):
        self.value = value
        self.name = name

class Address(_State):
    def __init__(self, Line1, City, Country, PostalCode, Line2=None, Line3=None, Line4=None, Line5=None, CountrySubDivision=None, Lat=None, Long=None):
        self.Line1 = Line1
        self.Line2 = Line2
        self.Line3 = Line3
        self.Line4 = Line4
        self.Line5 = Line5
        self.City = City
        self.Country = Country
        self.CountrySubDivisionCode = CountrySubDivision
        self.PostalCode = PostalCode
        self.Lat = Lat
        self.Long = Long

