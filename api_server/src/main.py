#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTPPException
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas
from api import appinfo

app = FastAPI()

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
@app.exception_handler(StarletteHTPPException)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=418,
        content={"message": exc.detail if hasattr(exc, 'detail') else str(exc)}
    )

app.include_router(appinfo.router, tags=["appinfo"])