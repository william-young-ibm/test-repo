import datetime as dt
import json
import pandas as pd
import numpy as np
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, func
from iotfunctions.base import BaseTransformer
from iotfunctions.metadata import EntityType
from iotfunctions.db import Database
from iotfunctions import ui

# <><><><>

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# <><><><>

print("got imports");
with open('credentials_as.json', encoding='utf-8') as F:
  credentials = json.loads(F.read())
print("Loaded creds")
db_schema = None
print(credentials);
db = Database(credentials=credentials, echo=True)
print("setup db");
from customWY.Email_Notification_WY import EmailNotificationWY
from customWY.Historian_Query_WY import HistorianQueryWY
from customWY.Maximo_Create_Work_Order_WY import MaximoCreateWorkOrderWY
from customWY.Maximo_Query_Last_PM_WY import MaximoQueryLastPMWY
from customWY.Maximo_Query_Work_Order_WY import MaximoQueryWorkOrderWY
print("registering");
db.register_functions([EmailNotificationWY, HistorianQueryWY, MaximoCreateWorkOrderWY, MaximoQueryLastPMWY, MaximoQueryWorkOrderWY])
print("registered");
