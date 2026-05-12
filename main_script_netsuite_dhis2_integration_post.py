#pip install requests requests_oauthlib

import requests
from requests_oauthlib import OAuth1
from datetime import datetime,date

# 🔹 Your NetSuite Account ID

# 🔹 Your Account ID
#ACCOUNT_ID = "4533524-sb1"
# 🔹 OAuth Credentials (use yours)

#CLIENT_KEY = "ab9235e9785c48173cdf356b7db4338c056c884dc465161372f582de68e7de2c"
#CLIENT_SECRET = "bca0d40e74b737e7d68096ae554f49d127450af9ca0e1c6b6e9e37cbf7e43835"
#TOKEN_ID = "d7563f9ac01bb8f1b5f82173387160fe2c76d590ece971da75cfcd5cbaa8d60e"
#TOKEN_SECRET = "A135c7fff25d3524238ff17ae8b06cf95ac58281d9736ecd3dbbc075e4da5747"


CLIENT_KEY = "94e71c68bb40ecd7ed764e005bedbe57d1cdb7a45a29a8b06bde6ba29a6f277c"
CLIENT_SECRET = "c88ae01cbbb3dd942bbd98e6619e3e54dccb70a1048da6f4b9fa6dbe552c6b23"
TOKEN_ID = "8cd2d33066bbe8313b2b5d8b28b6902ae1a6395c74d935ca783dd25f104559f1"
TOKEN_SECRET = "b2780b60182bc873d49ad45b56ce9b102835833e96c72ae563404067abd6029c"

#ACCOUNT_ID = "4533524_SB1"
  
#ACCOUNT_ID = "4533524-sb1"
BASE_URL = "https://4533524-sb1.suitetalk.api.netsuite.com"
ACCOUNT_ID = "4533524_SB1"  # underscore + uppercase
#"4533524_SB1"
# 🔹 OAuth1 Authentication
auth = OAuth1(
    CLIENT_KEY,
    CLIENT_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    signature_method='HMAC-SHA256',
    realm=ACCOUNT_ID
)


url = f"{BASE_URL}/services/rest/record/v1/vendor"

'''
payload = {
    "entityId": "SUPP1001",              # Supplier Code
    "companyName": "Test Supplier Pvt Ltd",
    "subsidiary": {"id": "33"},           # Required in OneWorld
    "email": "supplier@test.com",
    "phone": "9876543210",
    "currency": {"id": "1"}              # Optional but often required
}
'''
payload = {
    #"entityId": "SUPP2001",
    "companyname": "New Supplier Pvt Ltd",
    "category": {"id": "39"},
    "email": "supplier@test.com",
    "phone": "9876543210",
    "subsidiary": {"id": "33"},
    "custentity_jj_san_country_sup": {"id": "1"},
    "custentity_2663_email_address_notif" : "supplier@test.com",
    "payablesAccount": {"id": "3939"},
    "currency" :  {"id": "71"},
    #"defaultaddress" : "123 MG Road Mumbai 400001 INDIA",
    "addressBook": {
        "items": [
            {
                "defaultBilling": True,
                "defaultShipping": True,
                "addressBookAddress": {
                    "addr1": "123 MG Road",
                    "city": "Mumbai",
                    "state": "MH",
                    "zip": "400001",
                    "country": {"id": "IN"}
                }
            }
        ]
    },
    "custentity_ippf_uin_number": "UIN-778899"
}

#print(" post start" )
post_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Post start : { post_start } " )
print("-" * 50)
response = requests.post(
    url,
    auth=auth,
    json=payload,
    headers={"Content-Type": "application/json",
             "Accept": "application/json"}
)

# https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41233
# "entityId": "SUP8767 New Supplier Pvt Ltd",
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?q=entityId IS "SUP8765"
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41231
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?q=entityId IS "SUPP2001"
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41231

#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41231/addressBook
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41231/addressBook/61102
print("1 Status:", response.status_code)
#print("Response:", response.text)

#print("2 Status:", response.status_code)

if response.status_code == 204:
    print("Vendor created successfully.")
else:
    print("Response:", response.text)

#print("3 Status:", response.status_code)

if response.content:
    data = response.json()
    print(data)
else:
    print("Success - No content returned (204)")

#print("Location Header:", response.headers) 

location = response.headers.get("Location")
print("Location Header:", location)

if location:
    vendor_id = location.rstrip("/").split("/")[-1]
    print("Vendor Internal ID:", vendor_id)

    post_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Post end :  {post_end} " )
    print("-" * 50)

    get_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Get start : {get_start} ")
    print("-" * 50)
    created_supplier_response = requests.get(
        location,
        auth=auth,
        headers={"Accept": "application/json"}
    )

    if created_supplier_response.status_code == 200:
        get_response_data = created_supplier_response.json()

        entity_id_full = get_response_data.get("entityId")
        supplier_code = entity_id_full.split(" ")[0] if entity_id_full else None

        print("Full entityId:", entity_id_full)
        print("Supplier Code:", supplier_code)

        vendor_internal_id = get_response_data.get("id")
        uin_number = get_response_data.get("custentity_ippf_uin_number")
        email = get_response_data.get("email")
        payables_account_id = get_response_data.get("payablesAccount", {}).get("id")

        print("vendor_internal_id:", vendor_internal_id)
        print("uin_number:", uin_number)
        print("email:", email)
        print("payables_account_id:", payables_account_id)

    else:
        print("Error:", created_supplier_response.text)
    
    
    get_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("-" * 50)
    print(f"Get end : {get_end}" )
    print("-" * 50)


'''
from urllib.parse import urlparse
url = "https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/41233"

path = urlparse(url).path
vendor_id = path.split("/")[-1]

print(vendor_id)
'''


# 🔹 Example: Get Customers
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?limit=100
#url = f"https://{ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/record/v1/customer?limit=1"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer?limit=100"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/metadata-catalog"
#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor"

#url = f"https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer/3020"

#url = f"{BASE_URL}/services/rest/record/v1/customer/3020"
#url = f"{BASE_URL}/services/rest/record/v1/customer?limit=1"

#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/customer/3020

#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor?q=entityId IS "SUP121"
#https://4533524-sb1.suitetalk.api.netsuite.com/services/rest/record/v1/vendor/912

'''
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

#headers={"Accept": "application/json"}

response = requests.get(
    url,
    auth=auth,
    headers={"Accept": "application/json"}
)

#response = requests.get(url, auth=auth, headers=headers)
#response = requests.get(url, auth=auth)

print(response.status_code)
print(response.text)
#print("Response:", response.json())
'''

#NetSuite UI
#https://4533524-sb1.app.netsuite.com

#SuiteTalk (SOAP and REST web services)
#https://4533524-sb1.suitetalk.api.netsuite.com

#RESTlets
#https://4533524-sb1.restlets.api.netsuite.com

#External Forms
#https://4533524-sb1.extforms.netsuite.com

#data = response.json()   # Convert JSON to Python dict

''''
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
'''
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



#### post api

import requests
from requests_oauthlib import OAuth1

ACCOUNT_ID = "4533524_SB1"
BASE_URL = "https://4533524-sb1.suitetalk.api.netsuite.com"

auth = OAuth1(
    CLIENT_KEY,
    CLIENT_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    signature_method="HMAC-SHA256",
    realm=ACCOUNT_ID
)

url = f"{BASE_URL}/services/rest/record/v1/vendor"

payload = {
    "entityId": "SUPP1001",              # Supplier Code
    "companyName": "Test Supplier Pvt Ltd",
    "subsidiary": {"id": "1"},           # Required in OneWorld
    "email": "supplier@test.com",
    "phone": "9876543210",
    "currency": {"id": "1"}              # Optional but often required
}

response = requests.post(
    url,
    auth=auth,
    json=payload,
    headers={"Content-Type": "application/json",
             "Accept": "application/json"}
)

print("Status:", response.status_code)
print("Response:", response.text)

custentity_ippf_uin_number

payload = {
    "entityId": "SUPP1001",
    "companyName": "Test Supplier Pvt Ltd",
    "subsidiary": {"id": "1"},
    "custentity_ippf_uin_number": "UIN-778899"
}
custentity_ippf_uin_number
## final payloads for supplier post

payload = {
    #"entityId": "SUPP2001",
    "companyName": "New Supplier Pvt Ltd",
    "subsidiary": {"id": "33"},
    "email": "supplier@test.com",
    "phone": "9876543210",
    "category": {"id": "11"},
    "payablesAccount": {"id": "3939"},
    "custentity_2663_email_address_notif" : "supplier@test.com",
    "custentity_jj_san_country_sup": {"id": "1"},
    "custentity_ippf_uin_number": "UIN-778899",
    "addressBook": {
        "items": [
            {
                "defaultBilling": True,
                "defaultShipping": True,
                "addressBookAddress": {
                    "addr1": "123 MG Road",
                    "city": "Mumbai",
                    "state": "MH",
                    "zip": "400001",
                    "country": {"id": "IN"}
                }
            }
        ]
    }
}


# read  "entityId": "SUP8770 New Supplier Pvt Ltd"

data = response.json()
entity_id = data.get("entityId")
print("Entity ID:", entity_id)

# out-put -- SUP8770 New Supplier Pvt Ltd

supplier_code = data.get("entityId", "").split(" ")[0]
print("Supplier Code:", supplier_code)


## full code
response = session.get(vendor_url)

if response.status_code == 200:
    data = response.json()

    entity_id_full = data.get("entityId")
    supplier_code = entity_id_full.split(" ")[0] if entity_id_full else None

    print("Full entityId:", entity_id_full)
    print("Supplier Code:", supplier_code)
else:
    print("Error:", response.text)

    
vendor_internal_id = data.get("id")
uin_number = data.get("custentity_ippf_uin_number")
email = data.get("email")
payables_account_id = data.get("payablesAccount", {}).get("id")

'''