## 启动

```bash
docker-compose up -d
```

## 迁移数据库

```bash
docker-compose exec blog bash
python3 blog/blog/manage.py migrate
```

