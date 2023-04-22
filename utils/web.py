""" web utils """
import ipaddress
from typing import Dict
from urllib.parse import urlparse
from lxml import html

import requests
from requests.exceptions import Timeout
from readability import Document
from uuid import UUID


def parse_article(url: str) -> Dict:
    """
    Parses the HTML output for URL and grabs title and description
    :param url: The URL sent by the user
    :return: Dictionary containing HTML data
    """
    data = {"title": "", "description": "", "image": "", "body": ""}

    if not is_url(url):
        return data

    if is_url_blacklisted(url):
        return data

    try:
        headers = {'user-agent': 'Bookie/app'}
        response = requests.get(https_upgrade(url), timeout=3, headers=headers, verify=False)
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
        if is_url(image[0]):
            data["image"] = https_upgrade(image[0])
    if body:
        data["body"] = body

    return data


def is_url(url: str) -> bool:
    """
    Verify that a given url is a valid url
    :param domain: the url
    :return: If valid or not
    """
    try:
        u = urlparse(url)
    except Exception:
        return False

    try:
        int(u.netloc, 16)
        return False
    except ValueError:
        pass

    if (
        u.netloc != ""
        and u.scheme in ["http", "https"]
        and u.hostname is not None
        and len(u.hostname) < 63
        and u.hostname != "localhost"
        and u.username is None
        and u.password is None
    ):
        try:
            ipaddress.ip_address(u.hostname)
            return False
        except ValueError:
            pass

        return True

    return False


def https_upgrade(url: str) -> str:
    """
    Try To upgrade to HTTPS
    :param url: The URL sent by the user
    :return: The HTTP or HTTPS version
    """
    headers = {'user-agent': 'Bookie/app'}
    u = urlparse(url)
    if u.scheme != "" and u.scheme != "https" and u.netloc != "":
        https_url = f"https://{u.netloc}"
        try:
            resp = requests.get(https_url, allow_redirects=True, timeout=3, headers=headers, verify=False)
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