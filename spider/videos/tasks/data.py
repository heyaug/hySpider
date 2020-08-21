from spider.videos.celeryapp import data_app
from db.dbUtil import MongoDB

liVideoTable = MongoDB(db="videos", table="liVideoTest")
# 用mongodb保存json

@data_app.task(name='videos.data.li.Video')
def data_li_video(**kwargs):
    liVideo = kwargs.get("liVideo")
    # 取队列里key是liVideo的
    if liVideo:
        liVideoTable.updateOne(liVideo["contId"], liVideo)


@data_app.task(name='videos.data.li.Comment')
def data_li_comment(**kwargs):
    liComment = kwargs.get("liComment")
    if liComment:
        liVideoTable.updateOne(liComment["commentId"], liComment)
