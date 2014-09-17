import requests
from bs4 import BeautifulSoup


def hn_link_gen():
    """
    Grab all links off of hackernews
    yields them in a generator
    """
    resp = requests.get("http://news.ycombinator.com")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text)
    for item in soup.find_all('a'):
        yield item['href']


def gen_targets():
    for url in hn_link_gen():
        if not url.startswith('http'):
            continue
        if 'www.ycombinator.com' in url:
            continue
        else:
            split = url.split("://")
            domain = split[1].split("/")[0]
            yield "{0}://{1}".format(split[0], domain)

def gen_uniq_targets():
    targets = {}
    for url in gen_targets():
        if url not in targets:
            targets[url] = None
            yield url
