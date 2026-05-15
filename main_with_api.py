## install
#pip install python-dotenv
#pip install psycopg2-binary
#pip install clickhouse-connect
#pip install --upgrade certifi
#pip install --upgrade requests certifi urllib3 ## for post data in hmis production certificate issue

#python -m ensurepip --upgrade
#python -m pip install --upgrade pip setuptools wheel
#pip install fastapi uvicorn
#pip install fastapi uvicorn --no-cache-dir
#pip install --force-reinstall fastapi uvicorn

# run fast API
#uvicorn main:app --reload --host 0.0.0.0 --port 8000
#python -m uvicorn main_with_api:app --reload --host 0.0.0.0 --port 8000
#python -m uvicorn main:app --reload ## This bypasses the exe issue completely


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

#Create FastAPI app
app = FastAPI(title="DHIS2 OrgUnit API")


import urllib3 ## for disable warning of Certificate
urllib3.disable_warnings() ## for disable warning of Certificate

import ssl
#import requests

from concurrent.futures import ThreadPoolExecutor
import requests
import certifi  ## for post data in hmis production certificate issue
import json
from datetime import datetime,date
#import nepali_datetime
# main.py
from dotenv import load_dotenv
import os
import time

load_dotenv()

DHIS2_GET_API_URL = os.getenv("DHIS2_GET_API_URL")
DHIS2_GET_USER = os.getenv("DHIS2_GET_USER")
DHIS2_GET_PASSWORD = os.getenv("DHIS2_GET_PASSWORD")

DHIS2_POST_API_URL = os.getenv("DHIS2_POST_API_URL")
DHIS2_POST_USER = os.getenv("DHIS2_POST_USER")
DHIS2_POST_PASSWORD = os.getenv("DHIS2_POST_PASSWORD")

DHIS2_POST_API_URL_PRO = os.getenv("DHIS2_POST_API_URL_PRO")
DHIS2_POST_USER_PRO = os.getenv("DHIS2_POST_USER_PRO")
DHIS2_POST_PASSWORD_PRO = os.getenv("DHIS2_POST_PASSWORD_PRO")



# ✅ GLOBAL SESSIONS (only created once)
session_get = requests.Session()
session_post = requests.Session()
session_post_pro = requests.Session()

# Set auth once
session_get.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)
session_post.auth = (DHIS2_POST_USER, DHIS2_POST_PASSWORD)
session_post_pro.auth = (DHIS2_POST_USER_PRO, DHIS2_POST_PASSWORD_PRO)

#Create Request Model (VERY IMPORTANT)
class OrgUnitRequest(BaseModel):
    region_code: str
    legal_name: str
    uin_code: str
    tei_uid:str


from utils import (
    configure_logging,get_tei_details,get_orgunit_details, get_single_orgunit_details,get_orgunit_details_pro,
    log_info,log_error,get_org_and_child_uid,get_org_and_child_attribute_value,update_orgunit_in_dhis2_api,
    get_cached_orgunits,update_tei_attributeValue_in_dhis2_for_api,push_orgunit_in_dhis2_api,
    push_orgunit_in_dhis2,update_orgunit_in_dhis2
)

#print("OpenSSL version:", ssl.OPENSSL_VERSION)
#print("Certifi CA bundle:", requests.certs.where())



PROGRAM_UID = os.getenv("PROGRAM_UID")
PROGRAM_STAGE_UID = os.getenv("PROGRAM_STAGE_UID")
SEARCH_TEI_ATTRIBUTE_UID = os.getenv("SEARCH_TEI_ATTRIBUTE_UID")

UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID = os.getenv("UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID")
REGION_NAME_ATTRIBUTE_UID = os.getenv("REGION_NAME_ATTRIBUTE_UID")
LEGAL_NAME_ATTRIBUTE_UID = os.getenv("LEGAL_NAME_ATTRIBUTE_UID")

UIN_SYNC_BPR_DHIS2_ATTRIBUTE_PRO_UID = os.getenv("UIN_SYNC_BPR_DHIS2_ATTRIBUTE_PRO_UID")


SEARCH_VALUE = os.getenv("SEARCH_VALUE")
ORGUNIT_UID = os.getenv("ORGUNIT_UID")

ORG_UNIT_META_ATTRIBUTE = os.getenv("ORG_UNIT_META_ATTRIBUTE")
ORG_UNIT_META_ATTRIBUTE_PRO = os.getenv("ORG_UNIT_META_ATTRIBUTE_PRO")


orgunit_post_url = f"{DHIS2_POST_API_URL}organisationUnits"
orgunit_post_url_pro = f"{DHIS2_POST_API_URL_PRO}organisationUnits"
tei_get_url = f"{DHIS2_GET_API_URL}trackedEntityInstances"

dataValueSet_endPoint = f"{DHIS2_POST_API_URL}dataValueSets"

namespace_url = f"{DHIS2_GET_API_URL}dataStore/accuityResponse/"
ACCUITY_FLOW_URL = os.getenv("ACCUITY_FLOW_URL_NEW")
#print( f" DHIS2_GET_USER. { DHIS2_GET_USER }, DHIS2_GET_PASSWORD  { DHIS2_GET_PASSWORD} " )

#DHIS2_AUTH_POST = ("hispdev", "Devhisp@1")
#session_post = requests.Session()
#session_post.auth = DHIS2_AUTH_POST

# Create a session object for persistent connection
#session_get = requests.Session()
#session_get.auth = DHIS2_AUTH_GET

raw_auth = os.getenv("DHIS2_AUTH")

if raw_auth is None:
    raise ValueError("DHIS2_AUTH is missing in .env")

if ":" not in raw_auth:
    raise ValueError("DHIS2_AUTH must be in user:password format")

user, pwd = raw_auth.split(":", 1)
#session_get.auth = (user, pwd)
'''
session_get = requests.Session()
session_get.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)

session_post = requests.Session()
session_post.auth = (DHIS2_POST_USER, DHIS2_POST_PASSWORD)
'''

#session_get.verify = False

def process_single_orgunit_bpr(region_code, legal_name, uin_code, tei_uid):

    #orgunit_list_map = get_cached_orgunits(orgunit_post_url, session_post)
    orgunit_list_map = get_orgunit_details(orgunit_post_url, session_post)

    print(f"orgunit_list_map list Size {len(orgunit_list_map) }")
    log_info(f"orgunit_list_map list Size {len(orgunit_list_map) } ")

    parent_org_uid, orguit_uid, orguit_attribute_value = get_org_and_child_attribute_value(
        orgunit_list_map, region_code, ORG_UNIT_META_ATTRIBUTE,uin_code
    )

    if not parent_org_uid:
        return {
            "status": "error",
            "message": "Parent OrgUnit not found",
            "region_code": region_code
        }

    org_response = None

    # =========================
    # CREATE
    # =========================
    print("parent_org_uid: ", parent_org_uid)
    print("orguit_uid: ", orguit_uid)
    print("orguit_attribute_value: ", orguit_attribute_value)

    if orguit_attribute_value != uin_code:

        payload = {
            "name": legal_name,
            "shortName": uin_code,
            "parent": {"id": parent_org_uid},
            "openingDate": "1990-01-01",
            "attributeValues": [{
                "value": uin_code,
                "attribute": {"id": ORG_UNIT_META_ATTRIBUTE}
            }]
        }

        org_response = push_orgunit_in_dhis2_api(
            orgunit_post_url, session_post, payload,
            region_code, legal_name, uin_code
        )

    # =========================
    # UPDATE
    # =========================
    else:
        orgunit_data = get_single_orgunit_details(
            orgunit_post_url, session_post, orguit_uid
        )

        orgunit_data["name"] = legal_name
        orgunit_data["shortName"] = uin_code
        orgunit_data["attributeValues"] = [{
            "value": uin_code,
            "attribute": {"id": ORG_UNIT_META_ATTRIBUTE}
        }]

        org_response = update_orgunit_in_dhis2_api(
            orgunit_post_url, session_post, orgunit_data,
            orguit_uid, region_code, legal_name, uin_code
        )

    # =========================
    # TEI UPDATE
    # =========================
    tei_response = update_tei_attributeValue_in_dhis2_for_api(
        attribute_id=UIN_SYNC_BPR_DHIS2_ATTRIBUTE_UID,
        tei_uid=tei_uid,
        tei_get_url=tei_get_url,
        session_get=session_get
    )

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "status": "completed",
        "region_code": region_code,
        "legal_name": legal_name,
        "uin_code": uin_code,
        "orgunit": org_response,
        "tei_update": tei_response
    }

# =========================
# FOR IPPF Production
# =========================
def process_single_orgunit_pro(region_code, legal_name, uin_code, tei_uid):

    #orgunit_list_map = get_cached_orgunits(orgunit_post_url, session_post)
    orgunit_list_map = get_orgunit_details_pro(orgunit_post_url_pro, session_post_pro)

    print(f"orgunit_list_map list Size {len(orgunit_list_map) }")
    log_info(f"orgunit_list_map list Size {len(orgunit_list_map) } ")

    '''
    #s = "IPPF-AFG-001"
    parts = uin_code.split('-')   # ['IPPF', 'AFG', '001']
    second_part = parts[1]     # 'AFG'
    first_two_letters = second_part[:2]   # 'AF'
    print(first_two_letters)
    '''

    region_code_ippf_pro  = uin_code.split('-')[1][:2]

    parent_org_uid, orguit_uid, orguit_attribute_value = get_org_and_child_attribute_value(
        orgunit_list_map, region_code_ippf_pro, ORG_UNIT_META_ATTRIBUTE_PRO,uin_code
    )

    if not parent_org_uid:
        return {
            "status": "error",
            "message": "Parent OrgUnit not found",
            "region_code": region_code_ippf_pro
        }

    org_response = None

    # =========================
    # CREATE
    # =========================
    print("parent_org_uid: ", parent_org_uid)
    print("orguit_uid: ", orguit_uid)
    print("orguit_attribute_value: ", orguit_attribute_value)

    if orguit_attribute_value != uin_code:

        payload = {
            "name": legal_name,
            "shortName": uin_code,
            "parent": {"id": parent_org_uid},
            "openingDate": "1990-01-01",
            "attributeValues": [{
                "value": uin_code,
                "attribute": {"id": ORG_UNIT_META_ATTRIBUTE_PRO}
            }]
        }

        org_response = push_orgunit_in_dhis2_api(
            orgunit_post_url_pro, session_post_pro, payload,
            region_code_ippf_pro, legal_name, uin_code
        )

    # =========================
    # UPDATE
    # =========================
    else:
        orgunit_data = get_single_orgunit_details(
            orgunit_post_url_pro, session_post_pro, orguit_uid
        )

        orgunit_data["name"] = legal_name
        orgunit_data["shortName"] = uin_code
        orgunit_data["attributeValues"] = [{
            "value": uin_code,
            "attribute": {"id": ORG_UNIT_META_ATTRIBUTE_PRO}
        }]

        org_response = update_orgunit_in_dhis2_api(
            orgunit_post_url_pro, session_post_pro, orgunit_data,
            orguit_uid, region_code_ippf_pro, legal_name, uin_code
        )

    # =========================
    # TEI UPDATE
    # =========================
    tei_response = update_tei_attributeValue_in_dhis2_for_api(
        attribute_id=UIN_SYNC_BPR_DHIS2_ATTRIBUTE_PRO_UID,
        tei_uid=tei_uid,
        tei_get_url=tei_get_url,
        session_get=session_get
    )

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "status": "completed",
        "region_code": region_code_ippf_pro,
        "legal_name": legal_name,
        "uin_code": uin_code,
        "orgunit": org_response,
        "tei_update": tei_response
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_get = requests.Session()
    app.state.session_post = requests.Session()
    app.state.session_post_pro = requests.Session()

    app.state.session_get.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)
    app.state.session_post.auth = (DHIS2_POST_USER, DHIS2_POST_PASSWORD)
    app.state.session_post_pro.auth = (DHIS2_POST_USER_PRO, DHIS2_POST_PASSWORD_PRO)

    configure_logging()   # ✅ MUST BE HERE
    print("App started")
    log_info("App started")

    yield

    app.state.session_get.close()
    app.state.session_post.close()
    print("App stopped")
    log_info("App stopped")

# ✅ AFTER lifespan
app = FastAPI(lifespan=lifespan)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "https://links.hispindia.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### Not recommended for production.
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
@app.post("/orgunit-bpr")
def create_or_update_orgunit(request: OrgUnitRequest):

    print("API called")
    log_info("API called")

    result = process_single_orgunit_bpr(
        request.region_code,
        request.legal_name,
        request.uin_code,
        request.tei_uid
    )

     # 🔴 HANDLE ERROR PROPERLY
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result)

    return result

@app.post("/orgunit-pro")
def create_or_update_orgunit(request: OrgUnitRequest):

    print("API called")
    log_info("API called")

    result = process_single_orgunit_pro(
        request.region_code,
        request.legal_name,
        request.uin_code,
        request.tei_uid
    )

     # 🔴 HANDLE ERROR PROPERLY
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result)

    return result


'''    
@app.on_event("startup")
def startup_event():
    configure_logging()

@app.post("/orgunit")
def create_or_update_orgunit(request: OrgUnitRequest):

    log_info("API called")

    result = process_single_orgunit(
        request.region_code,
        request.legal_name,
        request.uin_code,
        request.tei_uid
    )

    # 🔴 HANDLE ERROR PROPERLY
    if result["status"] == "error":
        raise HTTPException(
            status_code=404,
            detail=result
        )

    return result
''' 