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
    start = time.time()
    url = "https://api.dhan.co/orders"

    headers = {
    "access-token": token,
    "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    
    # print(data)
    end = time.time()
    total = end - start
    print("getoderlist: ",total,"\n")
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
def placeorder(firstdict):
    start = time.time()
    if(firstdict['afterMarketOrder']==True):
        boolvalue = 'true'
    elif(firstdict['afterMarketOrder']==False):
        boolvalue = 'false'
    payload = f"{{\n \"dhanClientId\":\"{firstdict['dhanClientId']}\",\n \"correlationId\":\"{firstdict['correlationId']}\",\n \"transactionType\":\"{firstdict['transactionType']}\",\n \"exchangeSegment\":\"{firstdict['exchangeSegment']}\",\n \"productType\":\"{firstdict['productType']}\",\n \"orderType\":\"{firstdict['orderType']}\",\n \"validity\":\"{firstdict['validity']}\",\n \"tradingSymbol\":\"{firstdict['tradingSymbol']}\",\n \"securityId\":\"{firstdict['securityId']}\",\n \"quantity\":{firstdict['quantity']},\n \"disclosedQuantity\":{firstdict['disclosedQuantity']},\n \"price\": {firstdict['price']},\n \"triggerPrice\":{firstdict['triggerPrice']},\n \"afterMarketOrder\":{boolvalue},\n \"amoTime\": \"OPEN\",\n \"boProfitValue\":{firstdict['boProfitValue']},\n \"boStopLossValue\":{firstdict['boStopLossValue']},\n \"drvExpiryDate\":\"{firstdict['drvExpiryDate']}\",\n \"drvOptionType\":\"{firstdict['drvOptionType']}\",\n \"drvStrikePrice\": {firstdict['drvStrikePrice']}\n}}"
    print(payload)
    if(firstdict['productType']=='INTRADAY'):
            prevorder = postorder(payload,client1Token)
    end = time.time()
    total = end - start
    print("Placing order time: ", total)
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
    # Here is main function is starting.
    delay_seconds = 0
    #Geting the admin orderlist from the getorderlist function
    orderlist = getorderlist(adminToken)

    # Get the initial size of the orderlist
    openlistlen = len(orderlist)

    n = 0
    print(getorderlist(adminToken),"\n\n")
    print(getorderlist(client1Token))
    # while(1):
    #     start = time.time()
    #     orderlist = getorderlist(adminToken)
    #     corderlist = getorderlist(client1Token)
    #     if(len(orderlist)==0 and len(corderlist)==0):  
    #         continue
    #     firstdict = orderlist[0]
    #     cfirstdict = corderlist[0]
    #     time.sleep(delay_seconds)
    #     # n+=1
    #     # print(n)
    #     neworderlist = len(orderlist);
        
            
    #    # In this condition we check the admin orderlist is updated or not by the increase in the size of the list
    #     if(openlistlen < neworderlist):
    #         # If this condition was true which admin order stock means it reflect in the orderlist so order function will trigger
    #         placeorder(firstdict)
    #         openlistlen = neworderlist
        
    #     end = time.time()
    #     total = end - start
    #     print("Main Time complexity: ", total, "start time: ", start, "end time: ", end)
    
        # if(firstdict['orderStatus'] == 'CANCELLED'):
        #     cancelorder()
        # else:
        #     print("there is no orderwhich calculate this")

    
         
        
    
        

