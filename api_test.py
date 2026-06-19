import requests

#url = "http://your-server-ip:8000/orgunit"

url = "http://127.0.0.1:8000/orgunit-pro"
#url = "http://stage.hispindia.org:8000/orgunit-bpr"
#url = "http://45.79.125.242:8000/orgunit"

#url = "http://192.168.1.17:8000/orgunit"

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