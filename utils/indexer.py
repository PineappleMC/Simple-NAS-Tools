from typing import Any

from DrissionPage import Chromium
from DrissionPage._configs.chromium_options import ChromiumOptions
import urllib.parse

from DrissionPage._pages.session_page import SessionPage

co = ChromiumOptions()
co.set_browser_path(r'C:\Program Files\Twinkstar Browser\twinkstar.exe')

URL = 'https://www.1lou.me'

# bt之家搜索url格式化
def url_formator(keyword: str) -> str:
    standard_encoded = urllib.parse.quote(keyword, encoding='utf-8')
    custom_encoded = standard_encoded.replace('%', '_')
    route = f"{URL}/search-{custom_encoded}-1.htm"
    return route

def search(index: str) -> list[Any]:
    tab = Chromium(co).latest_tab
    tab.get(url_formator(index))

    results_list = []
    post_elements = tab.eles('css:li.media.thread.tap')

    for post in post_elements:
        link_tag = post.ele('css:div.subject > a')

        if link_tag:
            title = link_tag.text
            relative_url = link_tag.attr('href')
            full_url = urllib.parse.urljoin(URL, relative_url)
            tag_elements = post.eles('css:a.badge')
            tags_list = [tag.text for tag in tag_elements]
            post_data = {
                'title': title,
                'url': full_url,
                'tags': tags_list
            }
            results_list.append(post_data)
    return results_list

# torrent解析
def download_torrent(url: str) -> str | None:
    tab = Chromium(co).latest_tab
    tab.get(url)
    torrent_link_tag = tab.ele('css:ul.attachlist a', timeout=2)
    if torrent_link_tag:
        relative_url = torrent_link_tag.attr('href')
        full_url = urllib.parse.urljoin(URL, relative_url)
        ele = tab.ele('xpath://*[@id="body"]/div/div[2]/div/div[3]/div/div[2]/fieldset/ul/li/a')
        ele.click.to_download("../", "latest.torrent")
        ele.wait(10)
        return full_url
    else:
        return None


# print(download_torrent('https://www.1lou.me/thread-708724.htm'))