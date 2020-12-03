#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from mysql import MySQL
import os
import requests
import json
from pathlib import Path
import sys

# 测试MySQL
db = MySQL("localhost", "root", "root", "spark_store")

# 应用分类
cates = {
    "network": "网络应用",  
    "chat": "社交沟通",
    "music": "音乐欣赏",
    "video": "视频播放",
    "image_graphics": "图形图像",
    "games": "游戏娱乐",
    "office": "办公学习",
    "reading": "阅读翻译",
    "development": "编程开发",
    "tools": "系统工具",
    "themes": "主题美化",
    "others": "其他应用",
} 

# 应用文件目录
curr_dir = os.path.dirname(os.path.realpath(__file__))
json_dir = os.path.join(curr_dir, "json")

def create_category():
    """
    生成应用分类
    """
    for slug, name in cates.items():
        row = db.select_one("SELECT * FROM `spark_category` WHERE `slug`=%s", (slug))
        if row is None:
            db.execute("INSERT INTO `spark_category` (`slug`, `name`) VALUES(%s, %s)", (slug, name))

def download_json():
    """
    下载应用信息json文件
    """
    urls = [
        "https://json.jerrywang.top/store/network/applist.json",
        "https://json.jerrywang.top/store/chat/applist.json",
        "https://json.jerrywang.top/store/music/applist.json",
        "https://json.jerrywang.top/store/video/applist.json",
        "https://json.jerrywang.top/store/image_graphics/applist.json",
        "https://json.jerrywang.top/store/games/applist.json",
        "https://json.jerrywang.top/store/office/applist.json",
        "https://json.jerrywang.top/store/reading/applist.json",
        "https://json.jerrywang.top/store/development/applist.json",
        "https://json.jerrywang.top/store/tools/applist.json",
        "https://json.jerrywang.top/store/themes/applist.json",
        "https://json.jerrywang.top/store/others/applist.json",
    ]
    new_urls = dict(zip(cates.keys(), urls))
    
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)
    os.chdir(json_dir)
    for key, url in new_urls.items():
        print("开始下载：{0} : {1}".format(key, url))
        filename = "{0}.json".format(key)
        # file_path = os.path.join(json_dir, filename)    
        # if not os.path.exists(file_path):
        response = requests.get(url)
        content = response.content.decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        # else:
        #     print("文件{0}已存在，跳过".format(filename))
                
def extract_appinfo():
    """
    提取应用信息
    """
    if not os.path.exists(json_dir):
        print("请先下载应用信息！")
        return
    files = os.listdir(json_dir)
    os.chdir(json_dir)
    for filename in files:
        if filename == ".gitignore":
            continue
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f) # 单个分类的所有应用数据
            cate_name =  Path(filename).stem
            for item in data:
                insert_appinfo(item, cate_name)

def insert_appinfo(item, cate_name):
    """
    插入单个应用信息数据
    item 单个应用信息的数据 
        "Name": "Teamviewer",
        "Version": "15.10.5",
        "Filename": "teamviewer_15.10.5_amd64.deb",
        "Pkgname": "teamviewer",
        "Author": "teamviewer",
        "Contributor": "teamviewer",
        "Website": "www.teamviewer.com",
        "Update": "2020-10-01 15:19:03",
        "Size": "13.97 MB",
        "More": "跨平台的远程协助软件",
        "Tags": "deepin",
        "img_urls": "[\"https://examine-spark.oss-cn-shanghai.aliyuncs.com/images/2020/10/01/53deea30-03f9-11eb-9af6-a56dded7a25a.png\"]",
        "icons": "https://examine-spark.oss-cn-shanghai.aliyuncs.com/icons/2020/10/01/5e579430-03f9-11eb-9af6-a56dded7a25a.png"
    cate_id integer 应用分类ID
    """
    # 先查询应用信息是否存在
    row = db.select_one("SELECT * FROM `spark_appinfo` WHERE `pkgname`=%s", (item["Pkgname"]))
    if row is not None:
        print("{0} 应用已存在，无法插入！".format(item["Name"]))
        return
    sql = """
    INSERT INTO `spark_appinfo` (
        `category_id`, `name`, `pkgname`, `version`,
        `author`, `contributor`, `website`, `path`,
        `size`, `icon`, `tags`, `more`
    ) VALUES (
        %s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, %s, %s 
    )
"""
    cate_id = cates_data.get(cate_name, 0)
    if item.get("Filename") is not None:
        path = "store/{cate_name}/{pkgname}/{filename}".format( 
            cate_name=cate_name, 
            pkgname=item["Pkgname"], 
            filename=item.get("Filename")
        )
    else:
        path = ""
    icon = "https://cdn.jsdelivr.net/gh/Jerrywang959/jsonpng/store/{cate_name}/{pkgname}/icon.png" \
        .format(cate_name=cate_name, pkgname=item["Pkgname"])
    # icon = item.get("icons", icon)
    tags = item.get("Tags", "")
    values = (
        cate_id, item["Name"], item["Pkgname"], item["Version"],
        item["Author"], item["Contributor"], item["Website"], path,
        item["Size"], icon, tags, item["More"]
    )
    db.execute(sql, values)
     
    # 开始插入应用截图
    row = db.select_one("SELECT * FROM `spark_appinfo` WHERE `pkgname`=%s", (item["Pkgname"]))
    if row is None:
        print("{0} 应用插入失败！".format(item["Name"]))
        return
    imgUrls = item.get("img_urls", [])
    print("文件截图连接：{}".format(imgUrls))
    if isinstance(imgUrls, str) and imgUrls not in (""):
        imgUrls = json.loads(imgUrls)
        for img in imgUrls:
            db.execute("INSERT INTO `spark_screenshot` (`appid`, `url`) VALUES (%s, %s)", (row["id"], img))
    


    
if __name__ == "__main__":
    # 插入分类表数据
    create_category()
    
    # 下载json文件
    download_json()

    cates_data = db.select_all("SELECT id, slug FROM `spark_category` WHERE 1")
    cates_data = { item["slug"]: item["id"] for item in cates_data }
    
    # 提取应用信息
    extract_appinfo()
