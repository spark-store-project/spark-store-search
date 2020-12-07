#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path =  Path('.') / '.env' 
load_dotenv(dotenv_path)

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")