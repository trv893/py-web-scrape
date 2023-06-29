from basicScrape import fetch_url, parse_links
from bs4 import BeautifulSoup

def build_link_tree_and_scrape(root_url):
    link_tree = set()
    data = {}

    def traverse(url):
        if url in link_tree:
            return

        link_tree.add(url)

        html = fetch_url(url)
        if html is None:
            return

        data[url] = BeautifulSoup(html, "html.parser").get_text()

        for link in parse_links(html, url):
            traverse(link)

    traverse(root_url)
    return data
