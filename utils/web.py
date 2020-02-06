""" web utils """

from typing import Dict
import re
from lxml import html

import requests
from requests.exceptions import Timeout
from readability import Document
from urllib.parse import urlparse
from uuid import UUID


def parse_article(url: str) -> Dict:
    """
    Parses the HTML output for URL and grabs title and description
    :param url: The URL sent by the user
    :return: Dictionary containing HTML data
    """
    if is_url_blacklisted(url):
        return {}

    data = {"title": "", "description": "", "image": "", "body": ""}
    try:
        headers = {'user-agent': 'Bookie/app'}
        response = requests.get(https_upgrade(url), timeout=3, headers=headers)
    except Timeout:
        return data

    tree = html.fromstring(response.content)
    doc = Document(response.text)

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
    """
    Returns True if input is a URL
    :param url: The URL sent by the user
    :return: Return True if url is a URL, false if not
    """
    regex = re.compile(r"http[s]?:\/\/[a-zA-z\.\-0-9]+\.[a-zA-Z]+")
    exists = regex.search(url)
    if exists:
        return True

    return False


def https_upgrade(url: str) -> str:
    """
    Try To upgrade to HTTPS
    :param url: The URL sent by the user
    :return: The HTTP or HTTPS version
    """
    headers = {'user-agent': 'Bookie/app'}
    https_url = ""
    if url.lower().startswith("http://"):
        to_https = re.compile(re.escape('http://'), re.IGNORECASE)
        https_url = to_https.sub("https://", url)

    elif not url.lower().startswith("https://"):
        https_url = f"https://{url}"

    if https_url:
        try:
            resp = requests.get(https_url, allow_redirects=True, timeout=3, headers=headers)
        except Exception:
            return url
        if resp.status_code == 200:
            return https_url

    return url


def is_url_blacklisted(url: str) -> bool:
    """
    Check if URL is allowed to process.
    :param url: The URL sent by the user
    :return: True if blacklisted, False if not
    """
    blacklist = [
        "127.0.0.1",
        "169.254.169.254",
        "localhost",
    ]

    domain = urlparse(url).netloc.lower().split(":")[0]
    if domain in blacklist:
        return True
    return False


def is_valid_uuid(uuid: str, version=4):
    """
    Check if uuid is valid.
    :param uuid: The uuid to test
    :return: True if valid, False if not
    """
    try:
        uuid_obj = UUID(uuid, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid