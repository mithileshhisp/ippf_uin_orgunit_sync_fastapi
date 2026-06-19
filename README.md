# climate_data_exchange
python script to push aggregated data from Nepali Calendar to ISO Calendar 

Python Script to Auto sync Climet data from nepalhmis to dhis2 instance

# add flask for create web-app for DHIS2
## install

sudo apt install python3-pip

pip install flask requests python-dotenv

pip install --upgrade certifi

pip install --upgrade requests certifi urllib3

pip install flask-cors

pip install python-dotenv

pip install psycopg2-binary

pip install clickhouse-connect

pip install nepali-date_converter

pip install npdatetime

pip install datetime

#https://pypi.org/project/nepali-calendar-utils/

pip install nepali-calendar-utils

pip install nepali

pip install nepali-datetime


-- 
sudo apt update

sudo apt install python3-full python3-venv -y

-- Create virtual environment

cd /home/mithilesh/climet_data_exchange

python3 -m venv venv

-- Activate it

source venv/bin/activate

then

pip install nepali-datetime

pip install --upgrade requests certifi urllib3

pip install python-dotenv


-- now add cron inside that

-- Create virtual environment
cd /home/mithilesh/ippf_uin_orgunit_sync
python3 -m venv venv
-- Activate it
source venv/bin/activate

then
pip install python-dotenv
pip install --upgrade requests certifi urllib3
-- for run on putty
(venv) root@localhost:/home/mithilesh/ippf_uin_orgunit_sync# python main.py
cd /home/mithilesh/ippf_uin_orgunit_sync && /home/mithilesh/ippf_uin_orgunit_sync/venv/bin/python main.py

chmod +x /home/mithilesh/ippf_uin_orgunit_sync/main.py

chmod 755 /home/mithilesh/ippf_uin_orgunit_sync/logs
-- final schedular

55 11 * * * cd /home/mithilesh/ippf_uin_orgunit_sync && /home/mithilesh/ippf_uin_orgunit_sync/venv/bin/python main.py >> /home/mithilesh/ippf_uin_orgunit_sync/cronlogs_ippf_uin_orgunit_sync.log 2>&1


###############

this application Auto Sync/create the Organisationunit in new DHIS2 instance based on trackedentityinstance attribute value

and update the trackedentityinstance attribute value



##################################
# for FastAPI 

# python -m ensurepip --upgrade
# python -m pip install --upgrade pip setuptools wheel
# pip install fastapi uvicorn
# pip install fastapi uvicorn --no-cache-dir
# pip install --force-reinstall fastapi uvicorn

# pip install fastapi uvicorn requests python-dotenv gunicorn

# run fast API
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
# uvicorn main_with_api:app --host 0.0.0.0 --port 8000
# python -m uvicorn main_with_api:app --reload --host 0.0.0.0 --port 8000
# python -m uvicorn main:app --reload ## This bypasses the exe issue completely
# http://127.0.0.1:8000/docs
# https://stage.hispindia.org/docs#/


# setup on stage server

host name : stage.hispindia.org user: ********** pass: ********** port 22

-- Create virtual environment
# cd /home/mithilesh/ippf_uin_orgunit_sync_fastapi


# sudo apt update
# sudo apt install python3.12-venv -y

# python3 -m venv venv

# rm -rf venv   # delete old one


# -- Activate it
# source venv/bin/activate

# source venv/bin/activate
# apt install python3-pip
# pip install -r requirements.txt
# pip install python-dotenv
# sudo apt install python-dotenv
# pip install --upgrade pip
# pip install fastapi uvicorn requests python-dotenv
# pip install fastapi uvicorn requests python-dotenv gunicorn

# -- for start api 
# uvicorn main_with_api:app --host 0.0.0.0 --port 8000

# http://stage.hispindia.org:8000/docs
# http://45.79.125.242:8000/docs
# https://stage.hispindia.org/docs#/
# https://45.79.125.242/docs#/


-- Step-by-step: Run FastAPI in background (systemd)

-- ✅ 1. Stop current running server
CTRL + C

-- ✅ 2. Create systemd service file

sudo nano /etc/systemd/system/fastapi.service

-- ✍️ Paste this (IMPORTANT: update paths)

[Unit]
Description=FastAPI OrgUnit Service
After=network.target

[Service]
User=root
WorkingDirectory=/home/mithilesh/ippf_uin_orgunit_sync_fastapi
ExecStart=/home/mithilesh/ippf_uin_orgunit_sync_fastapi/venv/bin/uvicorn main_with_api:app --host 0.0.0.0 --port 8000

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

-- Check these paths:
ls /home/mithilesh/ippf_uin_orgunit_sync_fastapi/venv/bin/
-- You must see:
uvicorn
python

-- ✅ 3. Reload systemd
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

-- ✅ 4. Start service
sudo systemctl start fastapi

-- ✅ 5. Enable auto-start on reboot
sudo systemctl enable fastapi
Created symlink /etc/systemd/system/multi-user.target.wants/fastapi.service → /etc/systemd/system/fastapi.service.

-- ✅ 6. Check status
sudo systemctl status fastapi

-- You should see:
Active: active (running) ✅

-- 🛑 How to STOP (end) the service
sudo systemctl stop fastapi
👉 This immediately stops your FastAPI server

-- 🚫 Prevent it from auto-starting on reboot
sudo systemctl disable fastapi

-- 🔄 Restart (after code change)
sudo systemctl restart fastapi

-- 📊 Check status
sudo systemctl status fastapi

-- 🔍 Check logs (very useful)
journalctl -u fastapi -f

-- ❌ Completely remove service (if not needed)
sudo systemctl stop fastapi
sudo systemctl disable fastapi
sudo rm /etc/systemd/system/fastapi.service
sudo systemctl daemon-reload
