import requests

#url = "http://your-server-ip:8000/orgunit"

url = "http://******:8000/orgunit-pro"
#url = "http://******:8000/orgunit-bpr"
#url = "http://*******:8000/orgunit"

#url = "http://******:8000/orgunit"

payload = {
    "region_code": "ESEAOR",
    "legal_name": "Global Development Partners Foundation Ltd.",
    "uin_code": "IPPF-THA-008",
    "tei_uid": "drBWOwC30Zw"
}

response = requests.post(url, json=payload)

print(response.status_code)
#print(response.text)

print(response.json())