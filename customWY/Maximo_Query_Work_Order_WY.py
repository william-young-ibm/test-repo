import requests
import inspect
import logging
import datetime as dt
import smtplib, ssl
import math
from sqlalchemy.sql.sqltypes import TIMESTAMP,VARCHAR
import numpy as np
import pandas as pd

from iotfunctions.base import BaseTransformer
from iotfunctions import ui

logger = logging.getLogger(__name__)

PACKAGE_URL = 'git+https://git@github.com:william-young-ibm/test-repo.git'

class MaximoQueryWorkOrderWY(BaseTransformer):
    is_scope_enabled = True

    def __init__(self, asset_id, work_order_type, earliest_date, api_key):
        self.url = "https://gemas86.manage.gemas86.gtm-pat.com/maximo/api/os/REP_WORKORDER?lean=1&oslc.select=wonum&oslc.pageSize=1&oslc.where=assetnum=\"GN171050\"&oslc.where=worktype=\"PM\""
        self.work_order_type = work_order_type
        self.earliest_date = earliest_date
        self.api_key = api_key
        super().__init__()

    def execute(self, df):
        df = df.copy();
        payload={}
        headers = {'apikey': f'{self.api_key}'}
        response = requests.request("GET", self.url, headers=headers, data=payload)
        for i,input_item in enumerate(self.input_items):
            df[self.output_items[i]] = str(response.text)
        return df

    @classmethod
    def build_ui(cls):
        # define arguments that behave as function inputs
        inputs = []
        inputs.append(ui.UISingle(
            name = 'asset_id',
            datatype = str,
            description = "Asset ID to query workorders for.",
            required = True
        ))
        inputs.append(ui.UISingle(
            name = 'work_order_type',
            datatype = str,
            description = "Work order type to query for",
            required=True
        ))
        inputs.append(ui.UISingle(
            name = 'earliest_date',
            datatype = dt.datetime,
            description = "earliest date to search to",
            required=True
        ))
        inputs.append(ui.UISingle(
            name = "api_key",
            datatype = str,
            description = "Maximo API key",
            required = True
        ))

        outputs = []
        outputs.append(ui.UIFunctionOutSingle(
            name = 'pm_workorder',
            datatype = str
        ))

        return (inputs, outputs)
