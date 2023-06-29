import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise exception if status is not 200
    except Exception as e:
        print(f"Error fetching: {url} because of {e}")
        return None

    return response.text


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
