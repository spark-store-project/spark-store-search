#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import crud
import schemas
import models

router = APIRouter()


@router.get("/appinfo/search", response_model=List[schemas.AppItem])
def search(keyword: str, res: Response, db: Session = Depends(models.get_db)):
    """
    根据关键字搜索应用
    """
    if keyword.strip() == "":
        raise HTTPException(status_code=418, detail="搜索关键字不能为空！")

    apps = crud.search_app(db, keyword=keyword)
    res.status_code = 200
    return apps


@router.get("/appinfo/name", response_model=schemas.AppItem)
def appinfo(pkgname: str, db: Session = Depends(models.get_db)):
    """
    根据报名获取应用
    """
    if pkgname.strip() == "":
        raise HTTPException(status_code=418, detail="应用包名不能为空！")

    app = crud.get_app_item(db, pkgname=pkgname)
    return app


@router.get("/appinfo/list", response_model=List[schemas.AppItem])
def applist(page: int = 1, limit: int = 20, cate_name: str = "", db: Session = Depends(models.get_db)):
    """
    获取应用列表，默认查询所有应用，传入分类名称时，查询指定分类
    """
    cate_id = 0

    if page < 1:
        page = 1

    if cate_name != "":
        cates = crud.get_cates_slug(db)
        if cate_name not in cates:
            raise HTTPException(status_code=418, detail="无效的分类名称！")
        else:
            cate_id = cates[cate_name]

    skip = (page - 1) * limit
    return crud.get_app_list(db, skip, limit, cate_id)
