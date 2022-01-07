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

class MaximoQueryLastPMWY(BaseTransformer):
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
            name = 'asset_id',
            datatype = str,
            description = "Asset ID to query last PM for.",
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
            name = 'maximo_pm_found',
            datatype = bool,
            description = "False if no PM could be found for the given asset ID"
        ))
        outputs.append(ui.UIFunctionOutSingle(
            name = 'last_pm_datetime',
            datatype = dt.datetime
        ))

        return (inputs, outputs)
