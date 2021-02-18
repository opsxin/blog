# Blog

通过 [Django](https://www.djangoproject.com/) 搭建的个人[博客 opsxin](https://www.opsxin.com)，主要是为了~~卖卖广告~~使用 django。

## 快速部署

### 克隆项目

```bash
git clone https://github.com/opsxin/blog.git -b master
```

### 启动项目

切换路径到 *docker*

重命名*.env-sample* 为 *.env*，并修改其中的内容

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

#### 迁移数据库

```bash
docker-compose exec blog bash
python3 blog/blog/manage.py migrate
```

## 前端模板

模板文件路径：`subject/templates/subject`，~~因为对前端不熟悉，所以很丑，我知道:sob:~~，可以按照需求修改。

文章`article.html`，留言`contact.html`，首页`index.html`都基于`base.html`。

## 添加文章

进入 WEB 容器，*blog* 为`docker-compose.yaml`文件内定义的 service 名。

```bash
docker-compose exec blog bash
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
