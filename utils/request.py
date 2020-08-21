import requests
from lxml import html


def retry(times=1):
    """
    用来重试
    :param times:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = times
            while t > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"{func.__name__}:{e}")
                    t -= 1
        return wrapper
    return decorator


@retry(times=3)
def HtmlTree(url):
    headers = {'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               }
    htm = requests.get(url=url, headers=headers, timeout=10).content
    return html.etree.HTML(htm)


@retry(times=3)
def request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return requests.get(url=url, headers=headers, timeout=10)
