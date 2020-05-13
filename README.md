# Blog

通过 [Django](https://www.djangoproject.com/) 搭建的个人[博客 opsxin](https://www.opsxin.com)，主要是为了~~卖卖广告~~使用 django。

## 快速部署

### 克隆项目

```bash
git clone https://github.com/opsxin/blog.git -b master
```

### 回退项目

因为这个 Commit 包含了所有 Docker 所需的配置文件。也可以不回退项目，参考这个提交进行相应的文件修改即可。

```bash
git reset --hard 0d7c0c7985cf25f573a5d011a4d295fc703cabe5
```

### 配置环境

文件`.web.prod.env`或`.web.dev.env`，对应不同的线上环境，在`docker-compose.yaml`内设定使用那个配置文件。

```yaml
env_file:
  - ./.web.prod.env
```

### 配置数据库等

```ini
# DEBUG 模式，1 开启，0 关闭
DEBUG=1
# SECRET_KEY 建议自己修改
SECRET_KEY=45c251a0caa4fc73731a8cb64bc0eec6
# IP、域名
DJANGO_ALLOWED_HOSTS=127.0.0.1
# 暂时只支持配置为 mysql
DATABASE=mysql
# 数据库配置，用户名和密码需要和 docker-compose.yaml 文件同步配置
SQL_ENGINE=django.db.backends.mysql
SQL_DATABASE=blog
SQL_USER=blog
SQL_PASSWORD=123456
SQL_HOST=db
SQL_PORT=3306
# 如果 DEBUG 关闭时的静态文件目录，需和 docker-nginx.conf 文件同步配置
STATIC_ROOT=/static/
```

### 启动项目

#### 前台启动

```bash
docker-compose up
```

#### 后台启动

```bash
docker-compose up -d 
```

#### 配置文件或 Dockerfile 修改后启动

```bash
docker-compose up --build
```

## 前端模板

模板文件路径：`subject/templates/subject`，~~因为对前端不熟悉，所以很丑，我知道:sob:~~，可以按照需求修改。

文章`article.html`，留言`contact.html`，首页`index.html`都基于`base.html`。

## 添加文章

进入 WEB 容器，`web`为`docker-compose.yaml`文件内定义的 service 名。

```bash
docker-compose exec web bash
```

切换到`manage.py`文件所在路径。

```bash
cd blog
```

创建管理员账号，按照提示输入。

```bash
python manage.py createsuperuser
```

上述步骤完成后，浏览器访问管理员页面：`http://IP/admin/`，认证通过后添加文章即可。
