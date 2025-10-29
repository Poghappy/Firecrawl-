# 火鸟门户系统 - API接口集成与二次开发指南

> **文档版本**: v1.0
> **最后更新**: 2025-10-28
> **适用对象**: 二次开发人员、API对接工程师
> **技术栈**: PHP 7.2+, MySQL 5.6+, RESTful API

---

## 📚 目录

1. [开发环境准备](#一开发环境准备)
2. [系统架构概览](#二系统架构概览)
3. [核心配置文件](#三核心配置文件)
4. [数据库设计](#四数据库设计)
5. [API接口规范](#五api接口规范)
6. [常用功能开发](#六常用功能开发)
7. [计划任务开发](#七计划任务开发)
8. [安全规范](#八安全规范)
9. [性能优化](#九性能优化)
10. [调试技巧](#十调试技巧)

---

## 一、开发环境准备

### 1.1 本地开发环境搭建

#### Windows环境(推荐: PHPStudy)

```
1. 下载安装PHPStudy
   网址: https://www.xp.cn/

2. 配置PHP环境
   PHP版本: 7.4
   扩展:
     ✓ mysqli
     ✓ pdo_mysql
     ✓ gd
     ✓ curl
     ✓ fileinfo
     ✓ mbstring
     ✓ openssl
     ✓ redis (可选)

3. 配置MySQL
   版本: 5.7
   字符集: utf8mb4
   排序规则: utf8mb4_unicode_ci

4. 虚拟主机配置
   域名: local.firebird.com
   网站目录: D:\www\firebird\
   PHP版本: 7.4
```

#### Linux环境(推荐: Docker)

```bash
# 使用Docker一键部署开发环境
docker-compose up -d

# docker-compose.yml 示例
version: '3'
services:
  php:
    image: php:7.4-fpm
    volumes:
      - ./:/var/www/html

  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: firebird

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./:/var/www/html
      - ./nginx.conf:/etc/nginx/nginx.conf
```

### 1.2 开发工具推荐

#### IDE

```
推荐: PHPStorm (最强大)
  - 代码智能提示
  - 调试功能完善
  - 版本控制集成

替代: VSCode (轻量级)
  - 安装PHP扩展
  - 安装MySQL扩展
```

#### 调试工具

```
1. Xdebug (PHP调试)
   配置 php.ini:
     zend_extension=xdebug.so
     xdebug.remote_enable=1
     xdebug.remote_host=localhost
     xdebug.remote_port=9003

2. Postman (API测试)
   功能:
     - 模拟HTTP请求
     - 保存请求集合
     - 自动化测试

3. Navicat (数据库管理)
   功能:
     - 可视化数据库设计
     - SQL执行与调试
     - 数据导入导出
```

---

## 二、系统架构概览

### 2.1 目录结构

```
firebird/
├── api/                   # API接口目录
│   ├── v1/               # v1版本接口
│   ├── v2/               # v2版本接口
│   └── common/           # 公共API
│
├── app/                   # 应用核心
│   ├── controllers/      # 控制器
│   ├── models/           # 模型
│   ├── views/            # 视图(已弃用,改用template)
│   └── libraries/        # 核心类库
│
├── crons/                # 计划任务
│   ├── crons.php        # 任务调度器
│   ├── database_backup.php
│   └── order_check.php
│
├── data/                 # 数据目录
│   ├── config.inc.php   # 核心配置文件 ⭐
│   ├── cache/           # 缓存文件
│   ├── logs/            # 日志文件
│   └── backup/          # 备份文件
│
├── plugins/              # 插件目录
│   ├── payment/         # 支付插件
│   ├── sms/             # 短信插件
│   └── storage/         # 存储插件
│
├── template/             # 模板目录
│   ├── default/         # 默认模板
│   ├── mobile/          # 移动端模板
│   └── admin/           # 后台模板
│
├── upload/               # 上传文件
│   ├── images/
│   ├── files/
│   └── temp/
│
└── index.php            # 入口文件
```

### 2.2 MVC架构

```
请求流程:

  浏览器请求
      ↓
  index.php (路由分发)
      ↓
  Controller (控制器)
      ↓
  Model (数据模型)
      ↓
  Database (数据库)
      ↓
  Template (模板渲染)
      ↓
  HTML响应
```

---

## 三、核心配置文件

### 3.1 数据库配置

**文件**: `/data/config.inc.php`

```php
<?php
/**
 * 火鸟门户系统核心配置
 */

// 数据库配置
define('DB_HOST', 'localhost');        // 数据库主机
define('DB_PORT', '3306');             // 数据库端口
define('DB_NAME', 'firebird_portal');  // 数据库名
define('DB_USER', 'firebird');         // 数据库用户
define('DB_PASS', 'password');         // 数据库密码
define('DB_PREFIX', 'fb_');            // 表前缀

// 系统配置
define('SITE_URL', 'https://example.com');  // 网站URL
define('ADMIN_DIR', 'admin');               // 后台目录名
define('DEBUG_MODE', false);                // 调试模式(生产环境必须false)

// Redis配置(可选)
define('REDIS_HOST', '127.0.0.1');
define('REDIS_PORT', 6379);
define('REDIS_AUTH', '');                   // Redis密码

// 安全配置
define('AUTH_KEY', 'your-auth-key-here');   // 加密密钥(必须修改)
define('SALT', 'your-salt-here');           // 加密盐值(必须修改)

?>
```

### 3.2 自定义配置添加

```php
// 在 config.inc.php 末尾添加自定义配置

// 第三方API配置
define('THIRD_PARTY_API_KEY', 'your-api-key');
define('THIRD_PARTY_API_SECRET', 'your-api-secret');

// 功能开关
define('ENABLE_CACHE', true);          // 启用缓存
define('ENABLE_LOG', true);            // 启用日志
define('ENABLE_API', true);            // 启用API接口
```

---

## 四、数据库设计

### 4.1 核心数据表

#### 用户表 (fb_user)

```sql
CREATE TABLE `fb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码(MD5+SALT)',
  `mobile` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `realname` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `idcard` varchar(20) DEFAULT NULL COMMENT '身份证号',
  `balance` decimal(10,2) DEFAULT '0.00' COMMENT '余额',
  `points` int(11) DEFAULT '0' COMMENT '积分',
  `level_id` int(11) DEFAULT '1' COMMENT '等级ID',
  `status` tinyint(1) DEFAULT '1' COMMENT '状态 1正常 0禁用',
  `login_error_count` int(11) DEFAULT '0' COMMENT '登录错误次数',
  `last_login_time` int(11) DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) DEFAULT NULL COMMENT '最后登录IP',
  `create_time` int(11) NOT NULL COMMENT '注册时间',
  `update_time` int(11) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile` (`mobile`),
  KEY `status` (`status`),
  KEY `level_id` (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

#### 订单表 (fb_order)

```sql
CREATE TABLE `fb_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_sn` varchar(50) NOT NULL COMMENT '订单号',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `module` varchar(20) NOT NULL COMMENT '所属模块',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `pay_method` varchar(20) DEFAULT NULL COMMENT '支付方式',
  `pay_time` int(11) DEFAULT NULL COMMENT '支付时间',
  `status` tinyint(1) DEFAULT '0' COMMENT '订单状态 0待支付 1已支付 2已完成 -1已取消',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_sn` (`order_sn`),
  KEY `user_id` (`user_id`),
  KEY `status` (`status`),
  KEY `create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

### 4.2 数据库操作类

#### 基础查询

```php
<?php
// 引入数据库类
require_once APP_PATH . '/libraries/Database.php';

class UserModel {
    private $db;

    public function __construct() {
        $this->db = Database::getInstance();
    }

    /**
     * 根据ID获取用户信息
     */
    public function getUserById($id) {
        $sql = "SELECT * FROM fb_user WHERE id = :id";
        $params = [':id' => $id];
        return $this->db->getRow($sql, $params);
    }

    /**
     * 根据用户名获取用户
     */
    public function getUserByUsername($username) {
        $sql = "SELECT * FROM fb_user WHERE username = :username";
        $params = [':username' => $username];
        return $this->db->getRow($sql, $params);
    }

    /**
     * 获取用户列表
     */
    public function getUserList($page = 1, $limit = 20, $where = []) {
        $offset = ($page - 1) * $limit;

        $sql = "SELECT * FROM fb_user WHERE 1=1";
        $params = [];

        // 条件拼接
        if (!empty($where['status'])) {
            $sql .= " AND status = :status";
            $params[':status'] = $where['status'];
        }

        if (!empty($where['keyword'])) {
            $sql .= " AND (username LIKE :keyword OR mobile LIKE :keyword)";
            $params[':keyword'] = '%' . $where['keyword'] . '%';
        }

        $sql .= " ORDER BY id DESC LIMIT :offset, :limit";
        $params[':offset'] = $offset;
        $params[':limit'] = $limit;

        return $this->db->getAll($sql, $params);
    }

    /**
     * 创建用户
     */
    public function createUser($data) {
        $sql = "INSERT INTO fb_user
                (username, password, mobile, email, create_time)
                VALUES
                (:username, :password, :mobile, :email, :create_time)";

        $params = [
            ':username' => $data['username'],
            ':password' => md5($data['password'] . SALT),
            ':mobile' => $data['mobile'],
            ':email' => $data['email'] ?? '',
            ':create_time' => time()
        ];

        return $this->db->execute($sql, $params);
    }

    /**
     * 更新用户信息
     */
    public function updateUser($id, $data) {
        $fields = [];
        $params = [':id' => $id];

        foreach ($data as $key => $value) {
            $fields[] = "$key = :$key";
            $params[":$key"] = $value;
        }

        $sql = "UPDATE fb_user SET " . implode(', ', $fields) . " WHERE id = :id";

        return $this->db->execute($sql, $params);
    }

    /**
     * 删除用户
     */
    public function deleteUser($id) {
        $sql = "DELETE FROM fb_user WHERE id = :id";
        $params = [':id' => $id];
        return $this->db->execute($sql, $params);
    }
}
?>
```

---

## 五、API接口规范

### 5.1 RESTful API设计

#### 接口规范

```
基础URL: https://example.com/api/v1/

请求方法:
  GET    - 获取资源
  POST   - 创建资源
  PUT    - 更新资源(全量)
  PATCH  - 更新资源(部分)
  DELETE - 删除资源

响应格式: JSON

统一返回结构:
{
  "code": 200,           // 状态码 200成功 其他失败
  "message": "success",  // 提示信息
  "data": {}            // 返回数据
}
```

#### 状态码定义

```
200 - 成功
400 - 请求参数错误
401 - 未授权(未登录)
403 - 禁止访问(无权限)
404 - 资源不存在
500 - 服务器错误
```

### 5.2 API接口示例

#### 用户登录接口

```php
<?php
/**
 * 用户登录API
 * 文件: /api/v1/user/login.php
 */

header('Content-Type: application/json; charset=utf-8');

// 引入核心文件
require_once '../../data/config.inc.php';
require_once APP_PATH . '/libraries/Database.php';
require_once APP_PATH . '/models/UserModel.php';

// 获取POST参数
$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// 参数验证
if (empty($username) || empty($password)) {
    echo json_encode([
        'code' => 400,
        'message' => '用户名和密码不能为空',
        'data' => null
    ]);
    exit;
}

// 业务逻辑
try {
    $userModel = new UserModel();

    // 查询用户
    $user = $userModel->getUserByUsername($username);

    if (!$user) {
        throw new Exception('用户不存在');
    }

    // 验证密码
    if ($user['password'] !== md5($password . SALT)) {
        // 记录登录失败
        $userModel->updateUser($user['id'], [
            'login_error_count' => $user['login_error_count'] + 1
        ]);

        throw new Exception('密码错误');
    }

    // 检查账号状态
    if ($user['status'] != 1) {
        throw new Exception('账号已被禁用');
    }

    // 检查是否被锁定
    if ($user['login_error_count'] >= 5) {
        throw new Exception('账号已被锁定,请30分钟后重试');
    }

    // 登录成功,更新登录信息
    $userModel->updateUser($user['id'], [
        'login_error_count' => 0,
        'last_login_time' => time(),
        'last_login_ip' => $_SERVER['REMOTE_ADDR']
    ]);

    // 生成Token
    $token = generateToken($user['id']);

    // 返回成功
    echo json_encode([
        'code' => 200,
        'message' => '登录成功',
        'data' => [
            'user_id' => $user['id'],
            'username' => $user['username'],
            'mobile' => $user['mobile'],
            'token' => $token
        ]
    ]);

} catch (Exception $e) {
    echo json_encode([
        'code' => 400,
        'message' => $e->getMessage(),
        'data' => null
    ]);
}

/**
 * 生成Token
 */
function generateToken($userId) {
    $payload = [
        'user_id' => $userId,
        'exp' => time() + 7200  // 2小时有效期
    ];

    $token = base64_encode(json_encode($payload));
    $sign = md5($token . AUTH_KEY);

    return $token . '.' . $sign;
}
?>
```

#### 用户信息获取接口

```php
<?php
/**
 * 获取用户信息API
 * 文件: /api/v1/user/info.php
 */

header('Content-Type: application/json; charset=utf-8');

require_once '../../data/config.inc.php';
require_once APP_PATH . '/libraries/Database.php';
require_once APP_PATH . '/models/UserModel.php';

// Token验证
$token = $_SERVER['HTTP_AUTHORIZATION'] ?? '';

if (empty($token)) {
    echo json_encode([
        'code' => 401,
        'message' => '未登录',
        'data' => null
    ]);
    exit;
}

// 验证Token
$userId = verifyToken($token);

if (!$userId) {
    echo json_encode([
        'code' => 401,
        'message' => 'Token无效或已过期',
        'data' => null
    ]);
    exit;
}

// 获取用户信息
try {
    $userModel = new UserModel();
    $user = $userModel->getUserById($userId);

    if (!$user) {
        throw new Exception('用户不存在');
    }

    // 移除敏感信息
    unset($user['password']);
    unset($user['idcard']);

    echo json_encode([
        'code' => 200,
        'message' => 'success',
        'data' => $user
    ]);

} catch (Exception $e) {
    echo json_encode([
        'code' => 400,
        'message' => $e->getMessage(),
        'data' => null
    ]);
}

/**
 * 验证Token
 */
function verifyToken($tokenString) {
    $parts = explode('.', $tokenString);

    if (count($parts) != 2) {
        return false;
    }

    list($token, $sign) = $parts;

    // 验证签名
    if (md5($token . AUTH_KEY) !== $sign) {
        return false;
    }

    // 解析payload
    $payload = json_decode(base64_decode($token), true);

    // 检查是否过期
    if ($payload['exp'] < time()) {
        return false;
    }

    return $payload['user_id'];
}
?>
```

---

## 六、常用功能开发

### 6.1 短信发送功能

```php
<?php
/**
 * 短信发送类
 * 文件: /app/libraries/SmsService.php
 */

class SmsService {

    /**
     * 发送验证码短信
     */
    public static function sendVerifyCode($mobile, $code) {
        // 阿里云短信示例
        $accessKeyId = ALIYUN_ACCESS_KEY_ID;
        $accessKeySecret = ALIYUN_ACCESS_KEY_SECRET;
        $signName = '火鸟门户网';
        $templateCode = 'SMS_12345678';

        $params = [
            'code' => $code
        ];

        // 调用阿里云SDK
        $result = self::sendSms(
            $mobile,
            $signName,
            $templateCode,
            $params
        );

        // 记录日志
        self::logSms($mobile, $templateCode, $result);

        return $result;
    }

    /**
     * 调用阿里云短信接口
     */
    private static function sendSms($mobile, $signName, $templateCode, $params) {
        // 具体实现略...
        // 可使用阿里云官方SDK

        return [
            'success' => true,
            'message' => '发送成功'
        ];
    }

    /**
     * 记录短信日志
     */
    private static function logSms($mobile, $templateCode, $result) {
        $db = Database::getInstance();

        $sql = "INSERT INTO fb_sms_log
                (mobile, template_code, result, create_time)
                VALUES
                (:mobile, :template_code, :result, :create_time)";

        $params = [
            ':mobile' => $mobile,
            ':template_code' => $templateCode,
            ':result' => json_encode($result),
            ':create_time' => time()
        ];

        $db->execute($sql, $params);
    }
}
?>
```

### 6.2 文件上传功能

```php
<?php
/**
 * 文件上传类
 * 文件: /app/libraries/UploadService.php
 */

class UploadService {

    /**
     * 上传图片
     */
    public static function uploadImage($file, $dir = 'images') {
        // 验证
        if (!isset($file) || $file['error'] != 0) {
            throw new Exception('文件上传失败');
        }

        // 检查文件类型
        $allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!in_array($file['type'], $allowedTypes)) {
            throw new Exception('仅支持JPG/PNG/GIF格式');
        }

        // 检查文件大小(5MB)
        if ($file['size'] > 5 * 1024 * 1024) {
            throw new Exception('文件大小不能超过5MB');
        }

        // 生成文件名
        $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
        $filename = date('YmdHis') . '_' . uniqid() . '.' . $ext;

        // 目标目录
        $uploadDir = UPLOAD_PATH . '/' . $dir . '/' . date('Ym') . '/';

        // 创建目录
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0777, true);
        }

        // 移动文件
        $targetFile = $uploadDir . $filename;

        if (!move_uploaded_file($file['tmp_name'], $targetFile)) {
            throw new Exception('文件保存失败');
        }

        // 返回访问URL
        return str_replace(ROOT_PATH, '', $targetFile);
    }
}
?>
```

---

## 七、计划任务开发

### 7.1 自定义计划任务示例

```php
<?php
/**
 * 自动取消超时未支付订单
 * 文件: /crons/cancel_timeout_orders.php
 * 执行频率: 每30分钟
 */

// 防止直接访问
define('IN_CRONLITE', TRUE);

// 引入配置
require_once dirname(__FILE__) . '/../data/config.inc.php';
require_once APP_PATH . '/libraries/Database.php';

// 开始时间
$startTime = microtime(true);

// 日志文件
$logFile = LOG_PATH . '/cron_cancel_orders.log';

// 记录开始
file_put_contents($logFile, date('Y-m-d H:i:s') . " - 任务开始\n", FILE_APPEND);

try {
    $db = Database::getInstance();

    // 查询30分钟前创建且未支付的订单
    $timeout = time() - 30 * 60;

    $sql = "SELECT id, order_sn FROM fb_order
            WHERE status = 0
            AND create_time < :timeout";

    $orders = $db->getAll($sql, [':timeout' => $timeout]);

    $cancelCount = 0;

    foreach ($orders as $order) {
        // 更新订单状态为已取消
        $updateSql = "UPDATE fb_order
                     SET status = -1,
                         update_time = :update_time
                     WHERE id = :id";

        $result = $db->execute($updateSql, [
            ':id' => $order['id'],
            ':update_time' => time()
        ]);

        if ($result) {
            $cancelCount++;

            // 记录日志
            file_put_contents(
                $logFile,
                date('Y-m-d H:i:s') . " - 取消订单: {$order['order_sn']}\n",
                FILE_APPEND
            );
        }
    }

    // 统计
    $execTime = round(microtime(true) - $startTime, 2);
    $summary = "任务完成, 共处理 " . count($orders) . " 个订单, " .
               "取消 {$cancelCount} 个订单, 耗时 {$execTime} 秒";

    file_put_contents($logFile, date('Y-m-d H:i:s') . " - " . $summary . "\n\n", FILE_APPEND);

} catch (Exception $e) {
    // 错误处理
    $error = "任务执行失败: " . $e->getMessage();
    file_put_contents($logFile, date('Y-m-d H:i:s') . " - " . $error . "\n\n", FILE_APPEND);
}
?>
```

### 7.2 任务添加到系统

```sql
-- 在数据库中添加任务记录
INSERT INTO fb_cron_task
(name, filename, frequency, next_run_time, status)
VALUES
('取消超时订单', 'cancel_timeout_orders.php', 1800, UNIX_TIMESTAMP(), 1);

-- frequency: 执行间隔(秒) 1800 = 30分钟
-- status: 1=启用 0=禁用
```

---

## 八、安全规范

### 8.1 SQL注入防护

```php
// ❌ 错误示例(易受SQL注入攻击)
$id = $_GET['id'];
$sql = "SELECT * FROM fb_user WHERE id = $id";

// ✅ 正确示例(使用预处理)
$id = $_GET['id'];
$sql = "SELECT * FROM fb_user WHERE id = :id";
$params = [':id' => $id];
$user = $db->getRow($sql, $params);
```

### 8.2 XSS防护

```php
// 输出到HTML时必须转义
echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// 或使用框架提供的方法
echo e($userInput);  // Laravel风格
```

### 8.3 CSRF防护

```php
// 生成Token
$_SESSION['csrf_token'] = bin2hex(random_bytes(32));

// 表单中添加
<input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">

// 验证
if ($_POST['csrf_token'] !== $_SESSION['csrf_token']) {
    die('CSRF验证失败');
}
```

---

## 九、性能优化

### 9.1 使用Redis缓存

```php
<?php
/**
 * Redis缓存类
 */
class CacheService {
    private static $redis = null;

    public static function init() {
        if (!self::$redis) {
            self::$redis = new Redis();
            self::$redis->connect(REDIS_HOST, REDIS_PORT);

            if (REDIS_AUTH) {
                self::$redis->auth(REDIS_AUTH);
            }
        }
    }

    /**
     * 获取缓存
     */
    public static function get($key) {
        self::init();
        $value = self::$redis->get($key);
        return $value ? json_decode($value, true) : null;
    }

    /**
     * 设置缓存
     */
    public static function set($key, $value, $expire = 3600) {
        self::init();
        return self::$redis->setex($key, $expire, json_encode($value));
    }

    /**
     * 删除缓存
     */
    public static function delete($key) {
        self::init();
        return self::$redis->del($key);
    }
}

// 使用示例
$userId = 123;
$cacheKey = "user:{$userId}";

// 尝试从缓存获取
$user = CacheService::get($cacheKey);

if (!$user) {
    // 缓存未命中,从数据库查询
    $userModel = new UserModel();
    $user = $userModel->getUserById($userId);

    // 存入缓存(1小时)
    CacheService::set($cacheKey, $user, 3600);
}
?>
```

---

## 十、调试技巧

### 10.1 开启错误显示

```php
// 开发环境(仅本地)
if ($_SERVER['REMOTE_ADDR'] == '127.0.0.1') {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}
```

### 10.2 SQL调试

```php
// 输出SQL语句
echo $sql;
var_dump($params);

// 使用MySQL慢查询日志
// my.cnf:
// slow_query_log = 1
// long_query_time = 2  # 超过2秒的查询会被记录
```

### 10.3 API调试

```bash
# 使用curl测试API
curl -X POST https://example.com/api/v1/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"123456"}'

# 带Token请求
curl -X GET https://example.com/api/v1/user/info \
  -H "Authorization: Bearer your-token-here"
```

---

**开发建议**:

- 遵循PSR规范编写代码
- 所有函数/类必须有注释
- 敏感操作必须记录日志
- 定期code review
- 使用Git版本控制

**参考资料**:

- PHP官方文档: https://www.php.net/manual/zh/
- MySQL官方文档: https://dev.mysql.com/doc/
- 火鸟官方文档: https://help.kumanyun.com/
