import http.client
import time
import json
import requests
from datetime import datetime

# geting the validation datas
json_file_path = "D:\\linuxplayground\\Ben project conf\\data.json"

# Read data from the JSON file
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

adminToken = data['adminToken']
client1Token = data['client1Token']
previouseorder = 0

# Function to send the request GET order list from the api
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
    


# Function to get the order detail From the api.
def getorderdetail(token):
    # getting the latest order
    conn = http.client.HTTPSConnection("api.dhan.co")

    headers = {
    'access-token': token,
    'Accept': "application/json"
    }

    conn.request("GET", "/orders/", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


# Function to send a request Post order through API
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

# Function to Process and retriving a order detail and create the payload for the post order API 
def placeorder():
    orderlist = getorderlist(adminToken)
    firstdict = orderlist[0]
    if(firstdict['afterMarketOrder']==True):
        boolvalue = 'true'
    elif(firstdict['afterMarketOrder']==False):
        boolvalue = 'false'
    payload = f"{{\n \"dhanClientId\":\"{firstdict['dhanClientId']}\",\n \"correlationId\":\"{firstdict['correlationId']}\",\n \"transactionType\":\"{firstdict['transactionType']}\",\n \"exchangeSegment\":\"{firstdict['exchangeSegment']}\",\n \"productType\":\"{firstdict['productType']}\",\n \"orderType\":\"{firstdict['orderType']}\",\n \"validity\":\"{firstdict['validity']}\",\n \"tradingSymbol\":\"{firstdict['tradingSymbol']}\",\n \"securityId\":\"{firstdict['securityId']}\",\n \"quantity\":{firstdict['quantity']},\n \"disclosedQuantity\":{firstdict['disclosedQuantity']},\n \"price\": {firstdict['price']},\n \"triggerPrice\":{firstdict['triggerPrice']},\n \"afterMarketOrder\":{boolvalue},\n \"amoTime\": \"OPEN\",\n \"boProfitValue\":{firstdict['boProfitValue']},\n \"boStopLossValue\":{firstdict['boStopLossValue']},\n \"drvExpiryDate\":\"{firstdict['drvExpiryDate']}\",\n \"drvOptionType\":\"{firstdict['drvOptionType']}\",\n \"drvStrikePrice\": {firstdict['drvStrikePrice']}\n}}"
    print(payload)
    if(firstdict['productType']=='INTRADAY'):
            prevorder = postorder(payload,client1Token)
    return prevorder
        

    
# Function to send a POST request to API For the cancelling api
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
    

# Function to find the order in the client order list which admin cancel
def findorder(list_of_dicts, key, value):
    for index, dictionary in enumerate(list_of_dicts):
        if key in dictionary and dictionary[key] == value:
            return index
    return None

# Function to process the cancelorder 
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


if __name__ == "__main__":
    # # Here is main function is starting.
    # delay_seconds = 0.5
    # #Geting the admin orderlist from the getorderlist function
    # orderlist = getorderlist(adminToken)

    # # Get the initial size of the orderlist
    # openlistlen = len(orderlist)
    # firstdict = orderlist[0]

    # # Geting the OrderId from the client to prevent the duplicate order while looping
    # corderlist = getorderlist(client1Token)
    # cfirstdict = corderlist[0]
    # previouseorder = cfirstdict['orderId']

    # n = 0
    # while(1):
    #     # orderlist = getorderlist(adminToken)
    #     firstdict = orderlist[0]
    #     print(firstdict['orderId'])
    #     corderlist = getorderlist(client1Token)
    #     cfirstdict = corderlist[0]
    #     print(previouseorder)
    #     time.sleep(delay_seconds)
    #     n+=1
    #     print(n)
    
    #    # In this condition we check the admin orderlist is updated or not by the increase in the size of the list
    #     if(openlistlen < len(getorderlist(adminToken))):
    #         previouseorder = 0
    #         openlistlen = len(getorderlist(adminToken))
    #         # If this condition was true which admin order stock means it reflect in the orderlist so order function will trigger
    #         previouseorder = placeorder()
    
    # # This if statement is too verify and to avoid the duplicate entry of orders
    #     if(previouseorder == cfirstdict['orderId'] and openlistlen == len(getorderlist(adminToken))):
    #         continue 
    
    #     # if(firstdict['orderStatus'] == 'CANCELLED'):
    #     #     cancelorder()
    #     # else:
    #     #     print("there is no orderwhich calculate this")
    getorderlist(adminToken)
    placeorder()
    
         
        
    
        

