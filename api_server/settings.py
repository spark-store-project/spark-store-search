#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path =  Path('.') / '.env' 
load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
