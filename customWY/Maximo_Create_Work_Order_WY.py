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

PACKAGE_URL = 'https://github.com/william-young-ibm/test-repo.git'

class MaximoCreateWorkOrderWY(BaseTransformer):
    is_scope_enabled = True

    def __init__(self, asset_id, api_key):
        self.url = "https://gemas86.manage.gemas86.gtm-pat.com/maximo/api/os/mxapiwo?action=SAVETHISQUERY"
        self.asset_id = asset_id
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
            name = "api_key",
            datatype = str,
            description = "Maximo API key",
            required = True
        ))

        outputs = []
        outputs.append(ui.UIFunctionOutSingle(
            name = 'maximo_create_work_order_success',
            datatype = bool
        ))

        return (inputs, outputs)
