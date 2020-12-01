#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from sqlalchemy.orm import Session, joinedload
from typing import List

import models, schemas

def process_app_screenshot(appinfo: models.Appinfo):
    """
    处理appinfo应用数据
    """
    if hasattr(appinfo, "screenshots"): 
        imgs = []
        for img in appinfo.screenshots:
            imgs.append(img.url) 
        appinfo.imgs = imgs
    return appinfo

def process_cate_pair(cates: List[models.Category]):
    """
    处理category将slug为键，id为值
    """
    data = {}
    for cate in cates:
        data[cate.slug] = cate.id
    return data

#######################################################
# 应用搜索后端
#######################################################

def search_app(db: Session, keyword: str):
    search = "%{}%".format(keyword)
    apps = db.query(models.Appinfo) \
        .options(joinedload(models.Appinfo.screenshots)) \
        .options(joinedload(models.Appinfo.category)) \
        .filter(models.Appinfo.name.like(search)) \
        .order_by(models.Appinfo.order) \
        .all()
    res = []
    for app in apps:
        app = process_app_screenshot(app)
        app.category_slug = app.category.slug if app.category else  ""
        res.append(app)
    return res 

def get_app_item(db: Session, pkgname: str):
    app = db.query(models.Appinfo) \
        .options(joinedload(models.Appinfo.screenshots)) \
        .filter(models.Appinfo.pkgname == pkgname) \
        .first()
    app = process_app_screenshot(app)
    return app

def get_app_list(db: Session, skip: int, limit: int = 20, cate_id: int = 0):
    if cate_id != 0:
        query = db.query(models.Appinfo) \
            .options(joinedload(models.Appinfo.screenshots)) \
            .filter(models.Appinfo.category_id == cate_id) \
            .order_by(models.Appinfo.order).offset(skip).limit(limit)
    else:
        query = db.query(models.Appinfo) \
            .options(joinedload(models.Appinfo.screenshots)) \
            .order_by(models.Appinfo.order).offset(skip).limit(limit)
    
    apps = query.all()

    res = []
    for app in apps:
        app = process_app_screenshot(app)
        res.append(app)

    return res 

def get_cates_slug(db: Session):
    cates = db.query(models.Category).all()
    data = process_cate_pair(cates)
    return data
