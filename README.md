# 星火商店应用搜索功能开发

星火商店后端维持一个数据库，把所有的应用信息记录进去。然后写接口供商店客户端调用。      
应用信息表、应用截图表、应用分类表三个表基本上基本上就OK了        
直接用数据库记录好应用的数据，遍历仓库目录读取json，然后将信息写入数据库，写接口，然后客户端查。        
但是暂时我没有接触星火后端的权限，先用爬虫抓取应用数据，反正星火商店的应用数据都是开放的。      

数据库可能对并发的能力比较弱，要上缓存，或者限流。  

抓取好数据写入数据表后，然后投稿端添加新的应用，都要写入数据库。    
用flask写API供客户端使用，一个是应用信息查询，一个是应用信息录入。      

几个服务器路线：
```js
http://sucdn.jerrywang.top/
http://store.jerrywang.top/
http://dcstore.spark-app.store/
```

商店仓库地址 http://sucdn.jerrywang.top     
仓库应用信息项目地址 https://github.com/Jerrywang959/jsonpng  


# 应用信息抓取

```js
// 静态页面地址
http://sucdn.jerrywang.top/store/#/     
store/#/network
store/#/relations
store/#/musicandsound
store/#/videos
store/#/photos
store/#/games
store/#/office
store/#/reading
store/#/programming
store/#/tools
store/#/themes
store/#/others

// json 文件地址
网络应用 https://json.jerrywang.top/store/network/applist.json
社交沟通 https://json.jerrywang.top/store/chat/applist.json
音乐欣赏 https://json.jerrywang.top/store/music/applist.json
视频播放 https://json.jerrywang.top/store/video/applist.json
图形图像 https://json.jerrywang.top/store/image_graphics/applist.json
游戏娱乐 https://json.jerrywang.top/store/games/applist.json
办公学习 https://json.jerrywang.top/store/office/applist.json
阅读翻译 https://json.jerrywang.top/store/reading/applist.json
编程开发 https://json.jerrywang.top/store/development/applist.json
系统工具 https://json.jerrywang.top/store/tools/applist.json
主题美化 https://json.jerrywang.top/store/themes/applist.json
其他应用 https://json.jerrywang.top/store/others/applist.json

// 单个应用分析
应用信息下载地址 https://json.jerrywang.top/store/development/code/app.json 
应用图标 https://cdn.jsdelivr.net/gh/Jerrywang959/jsonpng/store/development/code/icon.png
应用下载地址 http://sucdn.jerrywang.top/store/development/code/code_1.49.0-1599744551_amd64.deb
```

单个应用信息json示例
```js
{
  "Name": "Visual Studio Code",
  "Version": "1.49.0-1599744551",
  "Filename": "code_1.49.0-1599744551_amd64.deb",
  "Pkgname": "code",
  "Author": "Microsoft",
  "Contributor": "Anysets",
  "Website": "https://code.visualstudio.com/",
  "Update": "2020-09-12 20:04:04",
  "Size": "61.57 MB",
  "More": "Visual Studio Code是一个运行于 Mac OS X、Windows和 Linux 之上的，针对于编写现代 Web 和云应用的跨平台源代码编辑器。该编辑器也集成了所有一款现代编辑器所应该具备的特性，包括语法高亮（syntax high lighting），可定制的热键绑定（customizable keyboard bindings），括号匹配（bracket matching）以及代码片段收集（snippets）。",
  "Tags": "",
  "img_urls": "[\"https://examine-spark.oss-cn-shanghai.aliyuncs.com/images/2020/09/12/c15c6380-f4ef-11ea-bf79-1335c9b78358.png\",\"https://examine-spark.oss-cn-shanghai.aliyuncs.com/images/2020/09/12/c3964df0-f4ef-11ea-bf79-1335c9b78358.png\"]",
  "icons": "https://examine-spark.oss-cn-shanghai.aliyuncs.com/icons/2020/09/12/bd3e4fc0-f4ef-11ea-bf79-1335c9b78358.png"
}
```

读取所有的json数据，然后分析提取，首先插入分类，然后插入截图，再插入应用信息。    
检测分类是否在分类表中，不在则新建该分类，然后拿到分类ID    
插入截图，拿到相应截图ID    
插入应用信息，拿到应用ID  
插入应用与截图关联信息  

# 数据表创建
应用信息表、应用截图表、应用分类表  
```sql
--- 应用信息表
CREATE TABLE `spark_appinfo` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `category_id` INT(11) NOT NULL COMMENT '所属分类',
  `name` VARCHAR(255) NOT NULL COMMENT '应用名称',
  `pkgname` VARCHAR(255) NOT NULL COMMENT '包名称',
  `version` VARCHAR(255) NOT NULL COMMENT '版本号',
  `author` VARCHAR(255) NOT NULL DEFAULT '未知' COMMENT '开发者',
  `contributor` VARCHAR(255) NOT NULL DEFAULT '未知' COMMENT '投稿人',
  `website` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '应用官网',
  `path` VARCHAR(500) NOT NULL COMMENT '文件下载路径',
  `size` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '大小',
  `icon` VARCHAR(500) NOT NULL DEFAULT '' COMMENT '图标',
  `tags` VARCHAR(500) NOT NULL DEFAULT '' COMMENT '标签',
  `more` TEXT COMMENT '详细及描述',
  `app_status` TINYINT(1) UNSIGNED NOT NULL DEFAULT '1' COMMENT '应用状态; 0: 下架, 1:正常, 2:未审核',
  `order` INT(11) NOT NULL DEFAULT '10000' COMMENT '排序',
	`created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
	`updated_at` TIMESTAMP NULL DEFAULT NULL COMMENT '最近一次修改时间',
  PRIMARY KEY (`id`),
  INDEX `category_id` (`category_id`)
)
COMMENT='应用信息表'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

--- 应用截图表
CREATE TABLE `spark_screenshot` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(500) NOT NULL COMMENT '图片链接',
  `order` INT(11) NOT NULL DEFAULT '10000' COMMENT '排序',
	`created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
)
COMMENT='应用截图表'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;


--- 应用应用与应用截图关联表
CREATE TABLE `spark_app_screenshot` (
  `appinfo_id` VARCHAR(500) NOT NULL COMMENT '应用ID',
  `screenshot_id` INT(11) NOT NULL COMMENT '截图ID',
  PRIMARY KEY `id` (`appinfo_id`, `screenshot_id`)
)
COMMENT='应用信息与应用截图关联表'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;


--- 应用分类表
CREATE TABLE `spark_category` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `slug` VARCHAR(50) NOT NULL COMMENT '分类标识',
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `order` INT(11) NOT NULL DEFAULT '10000' COMMENT '分类排序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
)
COMMENT='应用分类表'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;
```
