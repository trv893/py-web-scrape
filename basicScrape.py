import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        return None, str(e)

    return response.text, None


def parse_links(html, root_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and not href.startswith('#'):
            absolute_link = urljoin(root_url, href)
            if root_url in absolute_link:
                links.add(absolute_link)
    return links
