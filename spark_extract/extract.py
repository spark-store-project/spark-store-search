#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from mysql import MySQL
from urllib.request import urlopen
import os

# 测试MySQL
db = MySQL("localhost", "root", "root", "spark_store")

# 应用分类
cates = {
    "network": "网络应用",  
    "communication": "社交沟通",
    "music": "音乐欣赏",
    "videos": "视频播放",
    "graphics": "图形图像",
    "games": "游戏娱乐",
    "office": "办公学习",
    "translate": "阅读翻译",
    "development": "编程开发",
    "tools": "系统工具",
    "beautify": "主题美化",
    "others": "其他应用",
} 

def create_category():
    """
    生成应用分类
    """
    for slug, name in cates.items():
        row = db.select_one("SELECT * FROM `spark_category` WHERE `slug`=%s", (slug))
        if row is None:
            db.execute("INSERT INTO `spark_category` (`slug`, `name`) VALUES(%s, %s)", (slug, name))

def download_json():
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
    
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    json_dir = os.path.join(curr_dir, "json")
    os.chdir(json_dir)
    for key, url in new_urls.items():
        filename = "{0}.json".format(key)
        file_path = os.path.join(curr_dir, filename)    
        if not os.path.exists(file_path):
            response = urlopen(url)
            with open(filename, "w") as f:
                f.write(response.read().decode("gbk"))

    
if __name__ == "__main__":
    # 插入分类表数据
    create_category()
    
    # 下载json文件
    download_json()
