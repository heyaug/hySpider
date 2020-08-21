# hySpider

* 安装:

```shell
pip install -r requirements.txt
```

* 配置:

```shell
# config/setting.py
# 数据库和mq
RABBITMQ = {
    "host": "127.0.0.1",
    "user": "guest",
    "password": "guest"
}

```
* 启动

```shell
在hySpider目录下：
# 启动worker
celery worker -A spider.videos.celeryapp.app -l info -n app -P eventlet -Q videos.li --concurrency=70 -E
# 启动worker
celery worker -A spider.videos.celeryapp.data_app -l info -n data_app -P eventlet -Q videos.data.li --concurrency=70 -E
```
