import wikipedia
import re
import time
import os
import sys
import bz2
from collections import defaultdict
from codecs import open
from bs4 import BeautifulSoup
"""
A weird python script that tries to a walk a semi-random path
-
Made for entertainment purposes

In advance, wikipedia, I'm sowwy
I've added caching and restricted requests per timeframe, but I will be more or
less DDOSsing.
"""

# data structure for keeping track of where we went
visited = defaultdict(bool)

# init caching mechanism
if not os.path.exists('data'):
    os.makedirs('data')

# I want to store article names as files, so removing illegal characters is a must
illegal_filechars = re.compile(r'[\s#%&{}()\\/<>*@:"\'$!]')
def get_html(title):
    local_path = "data/%s.html.bz2" % illegal_filechars.sub('', title)
    # if cached
    if os.path.exists(local_path):
        with bz2.BZ2File(local_path, 'r') as f:
            return f.read()
        # with open(local_path) as f:
        #     return f.read()
    else:
        try:
            html = wikipedia.page(title).html()
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                html = wikipedia.page(e.options[0]).html()
            except:
                raise
        with bz2.BZ2File(local_path, 'w') as f:
            f.write(html.encode('utf8'))
        # with open(local_path, 'w+', 'utf-8') as f:
        #     f.write(html)
    return html

# wiki pages have info boxes, spam etc.
# it sucks
def remove_shit(soup):
    rm_classes = ["infobox", "toc", 'IPA', 'internal', 'extiw']
    for notebox in soup.find_all(True, {"class":rm_classes}):
        notebox.extract()

def filter_anchors(anchors):
    results = []
    for jump in anchors:
        try:
            title = jump['title']
            if any(jump['href'].startswith(junk) for junk in ['#', 'File:']) \
                or not title \
                or title.startswith("Special:") \
                or title.startswith("Edit section:") \
                or title.endswith("(page does not exist)"):
                continue
        except:
            continue

        if title and not visited[title]:
            results.append(title.strip())
    return results

def get_title_of_first_link_of_page(page_title):
    visited[page_title] = True

    html = get_html(page_title)
    soup = BeautifulSoup(html,'lxml')
    remove_shit(soup)
    titles = filter_anchors(soup.find_all('a'))
    if titles:
        return titles
    raise Exception("Couldn't find a valid link on this useless article")

if __name__ == '__main__':
    titles = ['Deterministic context-free language']

    while titles:
        title = titles.pop().strip()

        try:
            print(title)
            titles.extend(get_title_of_first_link_of_page(title)[::-1])
            if len(titles) > 100:
                titles = titles[-100:]
        except KeyboardInterrupt as e:
            print("You wanted me stopped, father :(\ny u do tis 2 me")
            exit(0)
        except Exception as e:
            print('fuck, article recovery failed me :/')
            #traceback.print_exc()
        time.sleep(1)

    print("No titles left to follow :/")
