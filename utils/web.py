""" web utils """

from typing import Dict
import re
from lxml import html

import requests
from readability import Document

def parse_article(url: str) -> Dict:
    """ Parses the HTML output for URL and grabs title and description """

    response = requests.get(https_upgrade(url))
    tree = html.fromstring(response.content)
    doc = Document(response.text)
    data = {"title": "", "description": "", "image": "", "body": ""}

    title = tree.xpath('//title/text()')
    description = tree.xpath('//meta[@name="description"]/@content')
    image = tree.xpath('//meta[@property="og:image"]/@content')
    body = doc.summary()

    if title:
        data["title"] = title[0]
    if description:
        data["description"] = description[0]
    if image:
        data["image"] = https_upgrade(image[0])
    if body:
        data["body"] = body

    return data


def is_url(url: str) -> bool:
    """ Returns True if input is a URL """
    regex = re.compile("http[s]?:\/\/[a-zA-z\.\-0-9]+\.[a-zA-Z]+")
    exists = regex.search(url)
    if exists:
        return True

    return False

def https_upgrade(url: str) -> str:
    """ Try to upgrade to HTTPS """
    if url.lower().startswith("http://"):
        to_https = re.compile(re.escape('http://'), re.IGNORECASE)
        https_url = to_https.sub("https://", url)
        try:
            resp = requests.get(https_url, allow_redirects=True)
        except Exception:
            return url
        if resp.status_code == 200:
            return https_url

    if not url.lower().startswith("https://"):
        https_url = f"https://{url}"
        try:
            resp = requests.get(https_url, allow_redirects=True)
        except Exception:
            return url
        if resp.status_code == 200:
            return https_url

    return url
