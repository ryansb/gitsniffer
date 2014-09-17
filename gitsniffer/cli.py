from collections import namedtuple
import click
import os
import pygit2
import requests
import sys


GitObj = namedtuple("GitObj", "fname prefix hash")


def hash_gen(index):
    for entry in index:
        fullhex = entry.hex
        fname = entry.path
        prefix, h = fullhex[0:2], fullhex[2:]
        yield GitObj(fname, prefix, h)


def download_file(fname, url):
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(fname, 'wb') as fd:
           for chunk in r.iter_content(256):
               fd.write(chunk)
        print("{0} --> {1}".format(url, fname))
    except:
        print("FAILED: {0}".format(url))

def make_dirs(*dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)

def grab_logs(url):
    log_jazz = ['logs/HEAD', "logs/refs/remotes/origin/HEAD", "logs/refs/heads/master"]
    make_dirs('logs', 'logs/refs', 'logs/refs/remotes', 'logs/refs/remotes/origin', 'logs/refs/heads')
    for log in log_jazz:
        download_file("./{0}".format(log), "{0}/{1}".format(url, log))


def grab_refs(url):
    make_dirs('refs', 'refs/heads', 'refs/remotes', 'refs/remotes/origin')
    ref_jazz = ['refs/heads/master', 'refs/remotes/origin/HEAD']
    for ref in ref_jazz:
        download_file("./{0}".format(ref), "{0}/{1}".format(url, ref))

def grab_meta(url):
    meta_files = ['COMMIT_EDITMSG', 'config', 'description',
                  'FETCH_HEAD', 'HEAD', 'index', 'ORIG_HEAD', 'packed-refs']
    for mf in meta_files:
        if os.path.exists(mf):
            print('Skipping: {0}/{1}'.format(url, mf))
            continue
        print('Grabbing {0}/{1}'.format(url, mf))
        download_file("./{0}".format(mf), "{0}/{1}".format(url, mf))

def grab_object(url, obj):
    obj_path = "objects/{0}/{1}".format(obj.prefix, obj.hash)
    if not os.path.exists("./objects/{0}".format(obj.prefix)):
        os.mkdir("./objects/{0}".format(obj.prefix))
    download_file("./{0}".format(obj_path), "{0}/{1}".format(url, obj_path))


@click.group()
def cli():
    pass


@cli.command(short_help="Scrape a URL")
@click.argument("url")
def run(url):
    if not os.path.exists('./.git'):
        os.mkdir('./.git')
    os.chdir('./.git')
    grab_meta(url)
    grab_refs(url)
    grab_logs(url)
    os.system("git init")
    repo = pygit2.Repository("./")
    for h in hash_gen(repo.index):
        grab_object(sys.argv[1], h)
