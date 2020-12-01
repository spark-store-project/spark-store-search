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
  INDEX `category_id` (`category_id`),
  UNIQUE INDEX `pkgname` (`pkgname`)
)
COMMENT='应用信息表'
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;

--- 应用截图表
CREATE TABLE `spark_screenshot` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `appid` INT(11) NOT NULL,
  `url` VARCHAR(500) NOT NULL COMMENT '图片链接',
  `order` INT(11) NOT NULL DEFAULT '10000' COMMENT '排序',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  INDEX `appid` (`appid`)
)
COMMENT='应用截图表'
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