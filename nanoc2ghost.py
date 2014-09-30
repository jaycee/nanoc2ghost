import os
from sys import argv
import datetime
import json

POST_INC = 0
EPOCH = datetime.datetime.fromtimestamp(0)
NOW = int((datetime.datetime.utcnow() - EPOCH).total_seconds() * 1000)


def make_post_data(title, date, body):
    global POST_INC
    POST_INC += 1
    post = {
        "id": POST_INC,
        "title": title,
        "slug": title.replace(' ', '-'),
        "markdown": body,
        "image": 'null',
        "featured": 0,
        "page": 0,
        "status": "published",
        "language": "en_US",
        "meta_title": 'null',
        "meta_description": 'null',
        "author_id": 1,
        "created_at": date,
        "created_by": 1,
        "published_at": date,
        "published_by": 1
    }
    return post


def process_file(filename):
    with file(filename) as f:
        data = f.read()
        _, meta, body = data.split('---\n')
    return meta, body


def process_meta(meta):
    post_date, title = meta.split('\n')[1:3]
    title = title.replace('title: ', '')
    post_date = post_date.replace('created_at: ', '')
    post_date = post_date.replace(' ', '')
    post_date = post_date.replace(',', '')
    if('am' in post_date.lower() or 'pm' in post_date.lower()):
        fmt = '%B%d%Y%I:%M%p'
    else:
        fmt = '%B%d%Y'
    post_date = datetime.datetime.strptime(post_date, fmt)
    post_date = int((post_date - EPOCH).total_seconds() * 1000)
    return title, post_date


def make_import_data(posts):
    return {
        "meta": {
            "exported_on": NOW,
            "version": "002"
        },
        "data": {
            "posts": posts,
            "tags": [],
            "posts_tags": [],
            "users": [],
            "roles_users": []
        }
    }

if __name__ == '__main__':
    files = os.listdir(argv[1])
    posts = []
    for f in files:
        meta, body = process_file(os.path.join(argv[1], f))
        title, post_date = process_meta(meta)
        post = make_post_data(title, post_date, body)
        posts.append(post)
    with file('output.json', 'w') as output:
        json.dump(make_import_data(posts), output)
