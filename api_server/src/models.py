#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import enum
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_size=300, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()

# 获取数据库实例
def get_db():
    try:
        db: Session = SessionLocal()
        # yield db
        return db
    finally:
        db.close()

# 枚举值
class AppStatus(enum.Enum):
    off = 0
    on = 1
    peding = 2

# 数据库模型类
class Appinfo(BaseModel):
    __tablename__ = "spark_appinfo"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("spark_category.id"))
    name = Column(String)
    pkgname = Column(String, unique=True, index=True)
    version = Column(String)
    author = Column(String)
    contributor = Column(String)
    website = Column(String)
    path = Column(String)
    size = Column(String)
    icon = Column(String)
    tags = Column(String)
    more = Column(Text)
    app_status = Column(TINYINT)
    order = Column(Integer)

    screenshots = relationship("Screenshot", backref='app')
    
    def __str__(self):
        return "Appinfo id={} name={}".format(self.id, self.name) 
    
class Category(BaseModel):
    __tablename__ = "spark_category"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    name = Column(String)

    apps = relationship('Appinfo', backref='category')

    def __str__(self):
        return "Category id={} name={}".format(self.id, self.name) 

class Screenshot(BaseModel):
    __tablename__ = "spark_screenshot"
    id = Column(Integer, primary_key=True, index=True)
    appid = Column(Integer, ForeignKey("spark_appinfo.id"))
    url = Column(String)
    order = Column(Integer)
    