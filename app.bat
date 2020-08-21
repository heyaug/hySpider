@ECHO OFF
rem 如果没代理，concurrency设置=1，否则封ip
rem celery worker -A spider.videos.celeryapp.app -l info -n app7 -P eventlet -Q videos.li --logfile=./log/app.log --concurrency=70 -E
celery worker -A spider.videos.celeryapp.app -l info -n app7 -P eventlet -Q videos.li --concurrency=70 -E