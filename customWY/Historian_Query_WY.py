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

class HistorianQueryWY(BaseTransformer):
    is_scope_enabled = True

    def __init__(self, input_items, output_items, url, api_key):

        self.input_items = input_items
        self.output_items = output_items
        self.url = url
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
            name = 'last_work_order_date',
            datatype = dt.datetime,
            description = "Datetime of the last submitted work order",
            required = True
        ))
        inputs.append(ui.UISingle(
            name = 'STATENUM',
            datatype = str,
            description = "STATENUM tag value",
            required = True
        ))
        inputs.append(ui.UISingle(
            name = "api_key",
            datatype = str,
            description = "Historian API key",
            required = True
        ))

        outputs = []
        outputs.append(ui.UIFunctionOutSingle(
            name = 'machine_time_running_hours_since_service',
            datatype = int
        ))

        return (inputs, outputs)
