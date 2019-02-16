""" web utils """

from typing import Dict
import re
from lxml import html
import requests

def parse_article(url: str) -> Dict:
    """ Parses the HTML output for URL and grabs title and description """

    response = requests.get(url)
    tree = html.fromstring(response.content)
    data = {"title": "", "description": "", "image": ""}

    title = tree.xpath('//title/text()')
    description = tree.xpath('//meta[@name="description"]/@content')
    image = tree.xpath('//meta[@property="og:image"]/@content')

    if title:
        data["title"] = title[0]
    if description:
        data["description"] = description[0]
    if image:
        data["image"] = image[0]

    return data


def is_url(url: str) -> bool:
    """ Returns True if input is a URL """
    regex = re.compile("http[s]?://[a-zA-z\.-]+\.[a-zA-Z]+")
    exists = regex.search(url)
    if exists:
        return True

    return False
