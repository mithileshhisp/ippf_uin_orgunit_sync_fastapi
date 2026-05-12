#pip install requests requests_oauthlib

import requests
from requests_oauthlib import OAuth1

from dotenv import load_dotenv
import os

load_dotenv()  # this loads .env file

# 🔹 Your NetSuite Account ID

# 🔹 Your Account ID
#ACCOUNT_ID = "******"
# 🔹 OAuth Credentials (use yours)

#CLIENT_KEY = "**********"
#CLIENT_SECRET = "***********"
#TOKEN_ID = "************"
#TOKEN_SECRET = "*********"

#signature_method='HMAC-SHA256',


CLIENT_KEY = os.getenv("CLIENT_KEY")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_ID = os.getenv("TOKEN_ID")
TOKEN_SECRET = os.getenv("TOKEN_SECRET")

NETSUITE_BASE_URL = os.getenv("NETSUITE_BASE_URL")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
SIGNATURE_METHOD = os.getenv("SIGNATURE_METHOD")

print("CLIENT_KEY:", CLIENT_KEY)

auth = OAuth1(
    CLIENT_KEY,
    CLIENT_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    signature_method=SIGNATURE_METHOD,
    realm=ACCOUNT_ID
)

# 🔹 Example: Get Customers
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?limit=100
#url = f"https://{ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/record/v1/customer?limit=1"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog/vendorcategory
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer?limit=100"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor"

#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer/3020"

#url = f"{BASE_URL}/services/rest/record/v1/customer/3020"
#url = f"{BASE_URL}/services/rest/record/v1/customer?limit=1"

#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer/3020

#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?q=entityId IS "SUP121"
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/912
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendorcategory/11

print("NETSUITE_BASE_URL:", NETSUITE_BASE_URL)

#url = f"{NETSUITE_BASE_URL}/services/rest/record/v1/customer?limit=10"
url = f"{NETSUITE_BASE_URL}/services/rest/record/v1/customer/3020"

print("URL:", url)

headers1 = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

headers={"Accept": "application/json"}

response = requests.get(
    url,
    auth=auth,
    headers=headers1
)

#response = requests.get(url, auth=auth, headers=headers)
#response = requests.get(url, auth=auth)

print(response.status_code)
#print(response.text)
#print("Response:", response.json())

#NetSuite UI
#https://4533524-sb1.app.netsuite.com

#SuiteTalk (SOAP and REST web services)
#https://4533524-sb1.suitetalk.api.netsuite.com

#RESTlets
#https://4533524-sb1.restlets.api.netsuite.com

#External Forms
#https://4533524-sb1.extforms.netsuite.com

data = response.json()   # Convert JSON to Python dict

'''
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer?limit=100"
#Access Top-Level Values

print(data["count"])          # 100
print(data["hasMore"])        # True
print(data["offset"])         # 0
print(data["totalResults"])   # 609

#Read Pagination Links
for link in data["links"]:
    print(link["rel"], ":", link["href"])

#only the next page URL:  
next_link = None

for link in data["links"]:
    if link["rel"] == "next":
        next_link = link["href"]

print("Next Page URL:", next_link) 

#Read All Customer IDs
#for item in data["items"]:
    #print(item["id"])

#Get Customer Self URL    

for item in data["items"]:
    customer_id = item["id"]
    self_url = item["links"][0]["href"]
    
    print("ID:", customer_id)
    print("URL:", self_url)

# Complete Working Example
#response = session.get(url)
#data = response.json()

print("Total Records:", data["totalResults"])

for item in data["items"]:
    customer_id = item["id"]
    print(customer_id)

# Pagination
if data["hasMore"]:
    for link in data["links"]:
        if link["rel"] == "next":
            next_url = link["href"]
            print("Next Page:", next_url)    



'''
#Read Simple Fields (Top Level)
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer/3020"

print("Customer ID:", data["id"])
print("Company Name:", data["companyName"])
print("Email:", data["email"])
print("Phone:", data["phone"])
print("Balance:", data["balance"])
print("Inactive:", data["isInactive"])
print("Created Date:", data["dateCreated"])
print("Last Modified:", data["lastModifiedDate"])

#Read Nested Objects

category_id = data["category"]["id"]
category_name = data["category"]["refName"]

print(category_id)
print(category_name)

#Currency
currency_id = data["currency"]["id"]
currency_name = data["currency"]["refName"]

print(currency_name)
currency_link = data["currency"]["links"][0]["href"]
print(currency_link)
currency_rel = data["currency"]["links"][0]["rel"]
print(currency_rel)

# Subsidiary
subsidiary_name = data["subsidiary"]["refName"]
print(subsidiary_name)

#Language
language = data["language"]["refName"]
print(language)

#Boolean Fields
print("Is Person:", data["isPerson"])
print("Unsubscribe:", data["unsubscribe"])
print("Direct Debit:", data["custentity_2663_direct_debit"])

# Read Links (Self URL)
self_url = data["links"][0]["href"]
print(self_url)

#Safe Way (Avoid KeyError)
email = data.get("email")
company = data.get("companyName")
category = data.get("category", {}).get("refName")

print(company, email, category)


'''
auth = OAuth1(
    client_key=CLIENT_KEY,
    client_secret=CLIENT_SECRET,
    resource_owner_key=TOKEN_ID,
    resource_owner_secret=TOKEN_SECRET,
    signature_method="HMAC-SHA256",
    realm=ACCOUNT_ID
)

auth = OAuth1(
    CLIENT_KEY.strip(),
    CLIENT_SECRET.strip(),
    TOKEN_ID.strip(),
    TOKEN_SECRET.strip(),
    signature_method='HMAC-SHA256',
    realm=ACCOUNT_ID
)

auth = OAuth1(
    client_key = CLIENT_KEY,
    client_secret = CLIENT_SECRET,
    resource_owner_key = TOKEN_ID,
    resource_owner_secret = TOKEN_SECRET,
    signature_method='HMAC-SHA256',
    realm=ACCOUNT_ID
)

print("Status:", response.status_code)
#data = response.json()
#print(data)


print("Status:", response.status_code)
print("Headers:", response.headers)
print(response.headers.get("Content-Type"))
print("Raw Text:")
print(response.text)

#print("Response:", response.json)



import requests
from requests_oauthlib import OAuth1

ACCOUNT_ID = "4533524_SB1"  # underscore for OAuth
BASE_URL = "https://4533524-sb1.suitetalk.api.netsuite.com"

auth = OAuth1(
    CLIENT_KEY,
    CLIENT_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    signature_method="HMAC-SHA256",
    realm=ACCOUNT_ID
)

url = f"{BASE_URL}/services/rest/record/v1/customer?limit=1"

headers = {
    "Accept": "application/json"
}

response = requests.get(url, auth=auth, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)


-- integration API
https://links.hispindia.org/ippf_uin/api/options?fields=id,name,code,attributeValues&filter=attributeValues.attribute.id:eq:ZoJYwqgoGI6&paging=false
https://links.hispindia.org/ippf_uin/api/trackedEntityInstances.json?ou=Eo4s43hL1Vi&ouMode=DESCENDANTS&program=w6sqrDv2VK8&filter=qZcVhl6kfpc:neq:%27%27

https://links.hispindia.org/ippf_uin/api/events.json?trackedEntityInstance=Fjdh85rHIQi&program=w6sqrDv2VK8&programStage=jKxGLMkHnHy&order=eventDate:desc&fields=event,orgUnit,eventDate,dataValues&skipPaging=true&filter=gDI26Sq88pk


https://links.hispindia.org/ippf_uin/api/events.json?trackedEntityInstance=Fjdh85rHIQi&program=w6sqrDv2VK8&programStage=HsKUiY7RyeO&order=eventDate:desc&fields=event,orgUnit,eventDate,dataValues&skipPaging=true&filter=TbN2rRfJxGs

'''