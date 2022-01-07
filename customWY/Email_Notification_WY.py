import inspect
import logging
import datetime as dt
import math
from sqlalchemy.sql.sqltypes import TIMESTAMP,VARCHAR
import numpy as np
import pandas as pd

import smtplib, ssl

from iotfunctions.base import BaseTransformer
from iotfunctions import ui

logger = logging.getLogger(__name__)

# Specify the URL to your package here.
# This URL must be accessible via pip install.
# Example assumes the repository is private.
# Replace XXXXXX with your personal access token.
# After @ you must specify a branch.

PACKAGE_URL = 'git+https://github.com/william-young-ibm/test-repo.git@main'

class EmailNotificationWY(BaseTransformer):
    is_scope_enabled = True

    def __init__(self, toEmail, subject, body, server, port, usingSSL, authentication, username, password, input_items, output_items):
        self.toEmail = toEmail
        self.subject = subject
        self.body = body
        self.server = server
        self.port = int(port)
        self.usingSSL = bool(usingSSL)
        self.authentication = bool(authentication)
        self.username = username
        self.password = password
        self.input_items = input_items
        self.output_items = output_items
        super().__init__()

    def execute(self, df):
        df = df.copy();
        formatted_message = f"Subject: { self.subject }\n\n{ self.body }"
        if self.usingSSL:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                if self.authentication:
                    server.login(self.username, self.password)
                server.sendmail(self.username, self.toEmail, formatted_message)
        else:
            with smtplib.SMTP(self.server, self.port) as server:
                if self.authentication:
                    server.login(self.username, self.password)
                server.sendmail(self.username, self.toEmail, formatted_message)
        for i,input_item in enumerate(self.input_items):
            df[self.output_items[i]] = df[input_item]
        return df



    @classmethod
    def build_ui(cls):
        #define arguments that behave as function inputs
        inputs = []
        inputs.append(ui.UISingle(
            name = 'toEmail',
            datatype = str,
            required = True,
            description = "Email destination for report"
        ))
        inputs.append(ui.UISingle(
            name = 'subject',
            datatype = str,
            required = True,
            description = "Subject line for email report"
        ))
        inputs.append(ui.UISingle(
            name = 'body',
            datatype = str,
            required = True,
            description = "Body for email report"
        ))
        inputs.append(ui.UISingle(
            name = 'server',
            datatype = str,
            required = True,
            description = "SMTP server to send email via"
        ))
        inputs.append(ui.UISingle(
            name = 'port',
            datatype = int,
            required = True,
            description = "SMTP port to use with server"
        ))
        inputs.append(ui.UISingle(
            name = 'usingSSL',
            datatype = bool,
            required = True,
            description = "Use SSL with SMTP server"
        ))
        inputs.append(ui.UISingle(
            name = 'authentication',
            datatype = bool,
            required = True,
            description = "Use authentication with SMTP server"
        ))
        inputs.append(ui.UISingle(
            name = 'username',
            datatype = str,
            required = False,
            description = "Username for SMTP authentication"
        ))
        inputs.append(ui.UISingle(
            name = 'password',
            datatype = str,
            required = False,
            description = "Password for SMTP authentication"
        ))
        inputs.append(ui.UIMultiItem(
            name = 'input_items',
            datatype=float,
            description = "Data items adjust",
            output_item = 'output_items',
            is_output_datatype_derived = True
        ))
        outputs = []
        return (inputs,outputs)
