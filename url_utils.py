import re
import validators
from bs4 import BeautifulSoup
import urllib.request

def validate(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return re.match(regex, url) is not None

def extract_content(url):
    """

    """
    if not validators.url(url):
        return ""
    web_url = urllib.request.urlopen(url)
    html = web_url.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()
