# Extract content from a wikinews dump file

import argparse
import logging
from bs4 import BeautifulSoup
import mwparserfromhell
import re
import json

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S %p',
                    level=logging.INFO)


def xml2dict(filename):
    with open(filename, 'r') as f:
        data = f.read()

    content = BeautifulSoup(data, "lxml")

    extracted = []
    pages = content.find_all('page')
    for page in pages:
        # BeautifulSoup content
        pageid = page.find('id').string
        title = page.find('title').string
        rawbody = page.find('text').string
        ns = page.find('ns').string

        if int(ns) != 0:
            continue

        # Regex extraction
        if is_redirect(rawbody):
            continue

        categories, rawbody = extract_categories(rawbody)
        dates, rawbody = extract_date(rawbody)
        rawbody = drop_sources(rawbody)

        # mwparserfromhell extraction
        parsedbody = mwparserfromhell.parse(rawbody)
        textbody = parsedbody.strip_code()

        # results
        extracted.append({
            'pageid': pageid,
            'title': title,
            'categories': categories,
            'dates': dates,
            'body': textbody
        })

    return extracted


def extract_categories(rawtext):
    pattern = re.compile("\[\[Categoria:([^\]]*)\]\]", re.IGNORECASE)
    try:
        matches = pattern.findall(rawtext)
        categories = [m for m in matches]
    except:
        categories = []

    try:
        content = pattern.sub('', rawtext)
    except:
        content = rawtext

    return categories, content


def extract_date(rawtext):
    pattern = re.compile("\{\{data\|([^\}]*)\}\}", re.IGNORECASE)
    try:
        matches = pattern.findall(rawtext)
        categories = [m for m in matches]
    except:
        categories = []

    try:
        content = pattern.sub('', rawtext)
    except:
        content = rawtext

    return categories, content


def drop_sources(rawtext):
    pattern = re.compile("\{\{Fonte\|[^\}]*\}\}", re.IGNORECASE)
    try:
        content = pattern.sub('', rawtext)
    except:
        content = rawtext

    return content


def is_redirect(rawtext):
    pattern = re.compile(".*#redirect \[\[[^\]]*\]\].*", re.IGNORECASE)
    try:
        found = pattern.search(rawtext)
        found = found != None
    except:
        found = False

    return found


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        default='content/raw/ptwikinews-20220401-pages-meta-current.xml',
                        help='Wikipedia xml dump file')

    parser.add_argument('--output', type=str,
                        default='content/json/wikinoticias_full.json',
                        help='Extracted content')

    args = parser.parse_args()

    logging.info(args)
    content = xml2dict(args.input)
    with open(args.output, 'w') as f:
        json.dump(content, f, indent=4)

    logging.info("Extracted {} articles".format(len(content)))
