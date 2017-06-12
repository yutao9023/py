from hashlib import md5


def get_md5(url):
    if isinstance(url, str):
        url = url.encode()
    m = md5()
    m.update(url)
    return m.hexdigest()

