import os


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)


def create_dirs(url, _dir=os.getcwd()):
    protocols = ["http://", "https://"]

    for protocol in protocols:
        if protocol in url:
            url = url[len(protocol):]
            break

    if "www." in url:
        url = url.replace("www.", "")

    if url[::-1][0] == "/":
        url = url[:len(url) - len("/")]

    url_split = url.split("/")

    if "." in url_split[-1]:
        url_split[-1] = url_split[-1][:url_split[-1].find(".")]

    path = _dir
    for name in url_split[:-1]:
        path += "\\" + name
        if not os.path.exists(path):
            os.mkdir(path)

    return os.path.join(path, url_split[-1])


def concatenate(lst):
    lst = [str(elem) for elem in lst]
    res = " ".join(lst)

    return res
