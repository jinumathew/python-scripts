#!/usr/bin/python
import requests
import json

#Getting the okta token for API calls.
def getOktaToken():
    url = "https://dev-706511.okta.com/oauth2/default/v1/token?scope=read&grant_type=client_credentials"
    oktaToken =''
    payload = {}
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic MG9hMmpkNGEycHFBNGVhYXU0eDY6SHVmQmRsSkdfclZBMzlydmJzSDJCRXVYN3g2VnFhdmdtemdhTFNORQ=='
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    #print(response.text.encode('utf8'))
    if(response.ok):
        data = response.json()
        token=data.get('access_token')
        if token:
            oktaToken = token                      
    return oktaToken

#Calling the REST API and verify the response.
def callLookkUpApi(token):
    #print("token: ",token)
    url = "https://reqresa.in/api/users"

    payload = "{\n    \"name\": \"morpheus\",\n    \"job\": \"leader\"\n}"
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+str(token) 
    }
    try:
        response = requests.request("POST", url, headers=headers, data = payload)
        if(response.ok):
            apiResponse = response.json()
            name=apiResponse.get('name')
            if name and (name == 'morpheus'):
                return True
            else:
                return False
        else:
            return False     
    except requests.exceptions.RequestException as err:
        print('Api Call error :', err)     
#sending the email alert for API failures
def sendEmailAlertsonFailures():
    print('sending failure email alets')

 #Executing the API calls   
print('starting the execution')
#apiToken=''
apiToken = getOktaToken()
if apiToken and (not apiToken.isspace()):
    lookupApiStatus = callLookkUpApi(apiToken)
    if (lookupApiStatus):
        print('Api is up and Running')
    else:
        sendEmailAlertsonFailures()
else:
    print("apitoken is empty")
print('completed')