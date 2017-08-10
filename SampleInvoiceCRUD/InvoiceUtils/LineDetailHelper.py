from SampleInvoiceCRUD.models import LineItem, SalesLineItem, DescriptionLineItem, DiscountLineItem, SubtotalLineItem, TaxLineItem, Ref

def createSalesLineItem(txn, Amount, Id=None, Description=None, LineNum=None, ItemRef=None, ClassRef=None, UnitPrice=None, Qty=None, ItemAccountRef=None, ServiceDate=None, TaxCode=None):
    detailType = "SalesItemLineDetail"
    line = LineItem(detailType, Amount, Id=Id,  LineNum=LineNum, Description=Description)

    salesItem = SalesLineItem()
    salesItem.ItemRef = createRefItem(salesItem.ItemRef, ItemRef)
    salesItem.ClassRef = createRefItem(salesItem.ClassRef, ClassRef)
    salesItem.ItemAccountRef = createRefItem(salesItem.ItemAccountRef, ItemAccountRef)
    salesItem.TaxCodeRef = createRefItem(salesItem.TaxCodeRef, TaxCode)
    salesItem.UnitPrice = UnitPrice
    salesItem.Qty = Qty
    salesItem.ServiceDate = ServiceDate

    line.SalesItemLineDetail = salesItem
    txn.Line.append(line)

def createDescriptionLineItem(txn, Amount, Id=None, Description=None, LineNum=None, TaxCodeRef=None, ServiceDate=None):
    detailType = "DescriptionOnly"
    line = LineItem(detailType, Amount, Id=Id,  LineNum=LineNum, Description=Description)

    descrItem = DescriptionLineItem()
    descrItem.ServiceDate = ServiceDate
    # descrItem.TaxCodeRef = Ref()
    descrItem.TaxCodeRef = createRefItem(descrItem.TaxCodeRef, TaxCodeRef)
    
    line.DescriptionLineDetail = descrItem
    txn.Line.append(line)

def createDiscountLineItem(txn, Amount, Id=None, Description=None, LineNum=None, TaxCodeRef=None, ClassRef=None, AccountRef=None, DiscountPercent=None):
    detailType = "DiscountLineDetail"
    line = LineItem(detailType, Amount, Id=Id,  LineNum=LineNum, Description=Description)
    
    dicountItem = DiscountLineItem()        
    if DiscountPercent is not None:
        dicountItem.PercentBased = True
    dicountItem.DiscountPercent = ServiceDate
    dicountItem.DiscountAccountRef = createRefItem(dicountItem.DiscountAccountRef, AccountRef)
    dicountItem.ClassRef = createRefItem(dicountItem.ClassRef, ClassRef)
    dicountItem.TaxCodeRef = createRefItem(dicountItem.TaxCodeRef, TaxCodeRef)
    line.DiscountLineDetail = dicountItem
    txn.Line.append(line)

def createSubtotalLineItem(txn, Amount, Id=None, Description=None, LineNum=None, ItemRef=None):
    detailType = "SubtotalLineDetail"
    line = LineItem(detailType, Amount, Id=Id,  LineNum=LineNum, Description=Description)  
    subtotalItem = SubtotalLineItem()
    subtotalItem.ItemRef = createRefItem(subtotalItem.ItemRef, AccountRef)
    line.SubtotalLineDetail = subtotalItem
    txn.Line.append(line)

#Helper function
def createRefItem(refItem, refField):
    if refField is not None:
        try:
            refItem=Ref(value=refField['value'])
        except:
            print('Please enter '+refItem+' as a dictionary')
        try:
            refItem.name = refField['name']
        except:
            refItem.name = None
    else:
        return refItem
    return refItem
