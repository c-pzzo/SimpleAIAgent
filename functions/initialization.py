#!/usr/bin/env python
# coding: utf-8

# # Instructions
# Este consiste en crear un pequeño AI Agent que lea la información de cualquier página web, encuentre la opción de facturar, vaya a la página de facturación y llene automáticamente el primer formulario encontrado con información aleatoria.
# 
# - Python 3.12.9

# # General strategy
# For every new billing site, this algorithm will learn the path to be followed needed to fill in its billing form. Once the path has already been defined and tested successfully, the path will be stored in a database for quick calling when a new bill is required from that business. For every successful execution, the metadata for latest date of successful execution will be updated. 
# 
# Two main libraries will be used:
# - Google's `Gemini` will provide the analysis of what's displayed in the website to make decisions. It will match user data and field information regardless of naming differences by following a detailed data dictionary.
# - The `Playwright` library will be used for Headless navigation of the billing site(s). 
# 
# Respectively, these libraries will be the brain and the hands used to explore the site. We also want to be mindful about the computational resources that we use, so we prioritize low computation functionalities, so I designed a simple workflow that will take into consideration if a site has already been visited, to run its pre-built instructions.
# 
# ## > Input:
# - JSON file with user and ticket data, as well as the root url to generate the invoice. 
# 
# ## > Output:
# - Screenshot of filled in billing form.
# 
# # Google Services:
# - Google Secrets Manager
# - Google Cloud Storage
# - FireStore
# - Gemini API
# - Google Cloud Build
# - Google Cloud Run

# # Libraries

# In[ ]:


# General
import io
import os
import json
import re
from datetime import datetime
import json

# Google Cloud Services
from google.auth import credentials
from google.oauth2 import service_account
from google.cloud import secretmanager, storage

# Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# Gemini
import google.generativeai as genai

# Playwright
import playwright

# FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException


# # Parameters

# In[16]:


sm_name = "projects/464704113649/secrets/main-keys/versions/3"


# # Initialization of Google Services

# ![Service Account](static/Services.png "Service Account of enabled Google Services")

# In[10]:


def initiate_secrets_manager(sm_name):
    sm_client = secretmanager.SecretManagerServiceClient()
    response = sm_client.access_secret_version(request={"name": sm_name})
    payload = response.payload.data.decode("UTF-8")
    env_vars = json.loads(payload)
    return env_vars


# # User-Defined Functions

# In[13]:


# Define global variables
env_vars = None
creds = None
db = None
mm_embedding_model = None
genai_model = None
storage_client = None
bucket_name = None
bucket = None

def initialize_services(sm_name):
    """Initialize services only once per Cloud Run instance"""
    global env_vars, creds, db, genai_model, storage_client, bucket_name, bucket

    env_vars = initiate_secrets_manager(sm_name)

    if creds is None:
        creds = service_account.Credentials.from_service_account_info(env_vars["zumma_service_account"])

    if not firebase_admin._apps:  # Avoid multiple Firebase initializations
        firebase_cred = credentials.Certificate(env_vars["zumma_service_account"])
        firebase_admin.initialize_app(firebase_cred)

    if db is None:
        db = firestore.client()

    if genai_model is None:
        genai.configure(api_key=env_vars['gemini_api_key'])
        genai_model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-lite")

    if storage_client is None:
        bucket_name = env_vars["bucket_name"]
        storage_client = storage.Client(credentials=creds)
        bucket = storage_client.bucket(bucket_name)


# In[17]:


# ✅ Call once at startup (e.g., in FastAPI `@app.on_event("startup")`)
initialize_services(sm_name)


# # Main
# 
# ## Input data
# Input: Json file with the following fields: <br>
# **User data**: <br>
# * "Razon_social": _Legal name of the company or individual_
# * "codigo_postal": _Postal code of the user's address_
# * "colonia": _"Neighborhood or subdivision within the city"_
# * "población": _City or town where the user is located_
# * "correo_electronico": _Email for invoice delivery_
# * "uso_de_cfdi": _Purpose of the invoice according to SAT (México)_
# * "delegacion_municipio": _Municipality or borough of the user's address_
# * "estado": _State where the user is located_
# * "regimen_fiscal": _Fiscal regime under which the user is registered_
# 
# **Ticket data**: <br>
# * "store_name": __
# * "store_address": __
# * "ticket_number": _(18 characters)_
# * "ticket_date": __
# * "ticket_total": _(Don't add tips)_
# * "billing_url": [_Primary Key_]
# 
# ## Relevant Libraries
# * `Gemini` has one task: Evaluate if the billing form url been reached. It will understand the webpage and make decisions using multimodal analysis (text and image) as needed.
# * `Playwright` has two tasks: to navigate to the path towards the billing form url, and to fill in the invoice. <br>
# 
# ## Steps
# Step 0. **Storage search**. <br> 
# In case that a business site has already been previously analyzed to call in the path to follow in Playwright.
# 
# Step 1. **Navigation**. <br> 
# 
# 1. Navigate on site: <br> 
# a) Analyze HTML<br>
# b) If information from previous step unclear, analyze site screenshot with Gemini's multimodal input.<br>
# 
# 2. Check if the billing form has been reached.<br>
# F) Update Playwright path & repeat cycle.<br>
# T) Go to next step<br>
# 
# Step 2. **Fill in Business form**. <br>
# a) New site: <br> 
# If successful execution, update `business_sites_directory` with a new entry for this site. Incorporate metadata with datetime of successful execution. <br>
# b) Site already in storage: <br> 
# Update datetime metadata with latest successful execution. This to keep track if site infrastructure changes. <br>

# In[ ]:




