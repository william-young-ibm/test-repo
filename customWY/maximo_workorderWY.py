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




PACKAGE_URL = 'git+https://github.com/william-young-ibm/test-repo.git@main'


class WorkOrdersWY(BaseTransformer):

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
        inputs.append(ui.UIMultiItem(
            name = 'input_items',
            datatype=str,
            description = "Data items adjust",
            output_item = 'output_items',
            is_output_datatype_derived = True
        ))
        inputs.append(ui.UISingle(
            name="url",
            datatype=str,
            description="What endpoint would you like to call?",
            required=True
        ))
        inputs.append(ui.UISingle(
            name="api_key",
            datatype=str,
            description="What is your api_key?",
            required=True
        ))

        outputs = []

        return (inputs, outputs)






