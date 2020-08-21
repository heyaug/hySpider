import hashlib
import re

import celery
import requests
import time

from db.dbUtil import MongoDB
from spider.videos.celeryapp import app, data_app
from utils.stringUtil import randomString


@app.task(
    name='videos.li.crawl',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='150/s',
)
def videoLi(self, url):
    try:
        XSerialNum = str(int(time.time()))
        XClientID = "861" + randomString(12)
        XClientHash = hashlib.md5((XSerialNum + XClientID).encode()).hexdigest()
        headers = {
            "X-Client-Version": "6.7.2",
            "X-Channel-Code": "lsp-yyb",
            "X-Client-Agent": "OneP9us_HD1910_5.1.1",
            "X-IMSI": "46000",
            "X-Long-Token": "",
            "X-Platform-Version": "5.1.1",
            "X-Client-Hash": XClientHash,
            "X-User-ID": "",
            "X-Platform-Type": "2",
            "X-Client-ID": XClientID,
            "X-Serial-Num": XSerialNum,
            "Host": "app.pearvideo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"}
        res = requests.get(url, headers=headers, timeout=5).json()
        resultCode = res.get("resultCode")
        # 根据resultCode，1 正常，5空数据，其他加入队列重新跑
        if resultCode == '1':
            content = res.get("content")
            data_app.send_task('videos.data.li.Video', kwargs={"liVideo": content})
            return
        if resultCode == '5':
            return
        raise Exception("no data")
    except Exception as e:
        celery.app.base.logger.warn(e)
        app.send_task("videos.li.crawl", args=(url,))


@app.task(
    name='videos.li.comment',
    bind=True,
    max_retries=8,
    retry_backoff=True,
    rate_limit='150/s',
)
def videoLiComment(self, commentUrl):
    try:
        XSerialNum = str(int(time.time()))
        XClientID = "861" + randomString(12)
        XClientHash = hashlib.md5((XSerialNum + XClientID).encode()).hexdigest()
        headers = {
            "X-Client-Version": "6.7.2",
            "X-Channel-Code": "lsp-yyb",
            "X-Client-Agent": "OneP9us_HD1910_5.1.1",
            "X-IMSI": "46000",
            "X-Long-Token": "",
            "X-Platform-Version": "5.1.1",
            "X-Client-Hash": XClientHash,
            "X-User-ID": "",
            "X-Platform-Type": "2",
            "X-Client-ID": XClientID,
            "X-Serial-Num": XSerialNum,
            "Host": "app.pearvideo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.11.0"}
        res = requests.get(commentUrl, headers=headers, timeout=5).json()
        resultCode = res.get("resultCode")
        commentList = res.get("commentList")
        nextUrl = res.get("nextUrl")
        # 用postId拼评论url
        postId = re.findall("postId=(\d+)?&", commentUrl)[0]
        if len(commentList) > 0:
            for comment in commentList:
                comment.update({"postId": postId})
                data_app.send_task('videos.data.li.Comment', kwargs={"liComment": comment})
            if nextUrl:
                app.send_task("videos.li.comment", args=(nextUrl,))
            return
        # 同上根据resultCode 判断
        if resultCode == '1' and len(commentList) == 0:
            return
        raise Exception
    except Exception as e:
        celery.app.base.logger.warn(e)
        app.send_task("videos.li.comment", args=(commentUrl,))


if __name__ == '__main__':
    def publishLiVideos():
        """
        id从1000000增加 穷举所有id
        :return:
        """
        for i in range(1000000, 1780000):
            li_url = f"http://app.pearvideo.com/clt/jsp/v4/content.jsp?contId={i}"
            app.send_task("videos.li.crawl", args=(li_url,))


    def publishVideoComments():
        postIds = set()
        # 从mongodb取数据，db=videos,table=liVideoTest，只取postId
        liVideoTable = MongoDB(db="videos", table="liVideoTest")
        for i in liVideoTable.con.find({}, {"postId": 1}):
            postId = i.get("postId")
            if postId and postId not in postIds:
                url = f"http://app.pearvideo.com/clt/jsp/v4/getComments.jsp?postId={postId}&score=&filterIds="
                app.send_task("videos.li.comment", args=(url,))
                postIds.add(postId)


    publishLiVideos()
    # publishVideoComments()
