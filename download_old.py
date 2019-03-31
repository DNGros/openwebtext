import multiprocessing as mp
from typing import Set

import newspaper
import os
import hashlib
import traceback
import tldextract
import tqdm
from filter import should_exclude

hash = hashlib.sha256

try:
    os.mkdir('data')
except FileExistsError:
    pass

# might not be threadsafe
past_text_hashes = set()


def dl(url):
    url = url.strip()

    if should_exclude(url):
        return

    ext = tldextract.extract(url)
    domain = '.'.join([x for x in ext if x])

    fname = 'data/{}-{}.txt'.format(domain, hash(url.encode()).hexdigest())
    if os.path.isfile(fname):
        return
#    print('Downloading', url)
    try:
        article = newspaper.Article(url, fetch_images=False)
        article.download()
        article.parse()
    except newspaper.article.ArticleException:
#        print('Dead link:', url)
        return
#        traceback.print_exc()

    text = article.text
    text_hash = hash(text.encode()).hexdigest()
    if past_text_hashes and text_hash in past_text_hashes:
        return

    if text.strip() == '':
#        print('Empty')
        return

    with open(fname, 'w') as out:
        out.write(text)
        past_text_hashes.add(text_hash)


if __name__ == '__main__':
    p = mp.Pool(40) # num of download threads
    with open('urls.txt') as fh:
        urls = list(fh)

        list(tqdm.tqdm(p.imap(dl, urls), total=len(urls)))
        print('Done!')
