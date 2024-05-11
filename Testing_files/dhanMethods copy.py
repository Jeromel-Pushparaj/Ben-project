import http.client
import time
import json
import requests
from datetime import datetime


adminToken = "" 
client1Token = ""
previouseorder = 0
def getorderlist(token):
    url = "https://api.dhan.co/orders"

    headers = {
    "access-token": token,
    "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    
    # print(data)
    return data
    



def getorderdetail():
    # getting the latest order
    conn = http.client.HTTPSConnection("api.dhan.co")

    headers = {
    'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzE1MDczNzYwLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDI1NDY4MiJ9.ufFsOvmIc8IEDDIq-N4vXayxHRAE4uCB4altQ5tiQLbOLW8Yv7TR7YVclH9-IVn2fDgCQwpMHm49QKSuDW3V8g",
    'Accept': "application/json"
    }

    conn.request("GET", "/orders/", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

# def dupordercheck(clienttoken):
    
    

def postorder(payload,clienttoken):
    #WITH EXTRACTED DATA WE ORDER FOR THE OTHER CLIENTS.

    conn = http.client.HTTPSConnection("api.dhan.co")

    headers = {
    'access-token': clienttoken,
    'Content-Type': "application/json",
    'Accept': "application/json"
    }

    conn.request("POST", "/orders", payload, headers)

    res = conn.getresponse()
    data = res.read()
    res = data.decode("utf-8")
    res_dict = json.loads(res)
    orderid = res_dict["orderId"]
    print(res)
    return orderid

def placeorder():
    orderlist = getorderlist(adminToken)
    firstdict = orderlist[0]
    if(firstdict['afterMarketOrder']==True):
        boolvalue = 'true'
    elif(firstdict['afterMarketOrder']==False):
        boolvalue = 'false'
    payload = f"{{\n \"dhanClientId\":\"{firstdict['dhanClientId']}\",\n \"correlationId\":\"{firstdict['correlationId']}\",\n \"transactionType\":\"{firstdict['transactionType']}\",\n \"exchangeSegment\":\"{firstdict['exchangeSegment']}\",\n \"productType\":\"{firstdict['productType']}\",\n \"orderType\":\"{firstdict['orderType']}\",\n \"validity\":\"{firstdict['validity']}\",\n \"tradingSymbol\":\"{firstdict['tradingSymbol']}\",\n \"securityId\":\"{firstdict['securityId']}\",\n \"quantity\":{firstdict['quantity']},\n \"disclosedQuantity\":{firstdict['disclosedQuantity']},\n \"price\": {firstdict['price']},\n \"triggerPrice\":{firstdict['triggerPrice']},\n \"afterMarketOrder\":{boolvalue},\n \"amoTime\": \"OPEN\",\n \"boProfitValue\":{firstdict['boProfitValue']},\n \"boStopLossValue\":{firstdict['boStopLossValue']},\n \"drvExpiryDate\":\"{firstdict['drvExpiryDate']}\",\n \"drvOptionType\":\"{firstdict['drvOptionType']}\",\n \"drvStrikePrice\": {firstdict['drvStrikePrice']}\n}}"
    if(firstdict['productType']=='INTRADAY'):
            prevorder = postorder(payload,client1Token)
    return prevorder
        

    

def postcancelorder(orderid,clienttoken):


    conn = http.client.HTTPSConnection("api.dhan.co")

    headers = {
    'access-token': clienttoken,
    'Accept': "application/json"
    }

    conn.request("DELETE", f"/orders/{orderid}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def findorder(list_of_dicts, key, value):
    for index, dictionary in enumerate(list_of_dicts):
        if key in dictionary and dictionary[key] == value:
            return index
    return None

def cancelorder():
    orderList = getorderlist(adminToken)
    firstdict = orderList[0]
    valuetradingsymbol = firstdict['tradingSymbol']
    clientOrderList = getorderlist(client1Token)
    indexToCancel = findorder(clientOrderList,'tradingSymbol',valuetradingsymbol)
    orderToCancel = clientOrderList[indexToCancel]
    orderid = orderToCancel['orderId']
    postcancelorder(orderid, client1Token)
    
    
    

    
# n =0
# while(1):
#     orderlist = getorderlist(client1Token)
#     firstdict = orderlist[0]
#     cancelorder(firstdict['orderId'])
#     n+=1




delay_seconds = 0.5

orderlist = getorderlist(adminToken)
openlistlen = len(orderlist)
firstdict = orderlist[0]

corderlist = getorderlist(client1Token)
cfirstdict = corderlist[0]
previouseorder = cfirstdict['orderId']


while(1):
    # orderlist = getorderlist(adminToken)
    firstdict = orderlist[0]
    corderlist = getorderlist(client1Token)
    cfirstdict = corderlist[0]
    print(previouseorder)
    time.sleep(delay_seconds)
    if(openlistlen < len(getorderlist(adminToken))):
        previouseorder = 0
        openlistlen = len(getorderlist(adminToken))
        previouseorder = placeorder()
    if(previouseorder == cfirstdict['orderId'] and openlistlen == len(getorderlist(adminToken))):
        continue 
    # if(firstdict['orderStatus'] == 'CANCELLED'):
    #     cancelorder()
    # else:
    #     print("there is no orderwhich calculate this")
    
        

