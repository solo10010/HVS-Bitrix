import requests
import re
import asyncio
import json
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, url_list=[]):
        self.url_list = url_list
        self.ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.self_scripts = {
            "ajax": r'\$.ajax\s*\((.*\{[^}]*\})',
            "get": r'\$.get\s*\((.*\{[^}]*\})',
            "post": r'\$.post\s*\((.*\{[^}]*\})',
        }
        self.__output = {}

    def __get_html_code(self, url: str):
        try:
            response = requests.get(url, headers={"user-agent": self.ua})
            response.raise_for_status()
            if 'html' in response.headers['content-type']:
                return response.text
            else:
                return "null"
        except requests.RequestException as e:
            print(f"Cannot parse url: {url}, Error: {e}")
            return "null"

    def __found_self_scripts(self, type_js: str, value: str, url: str) -> None:
        html_code = self.__get_html_code(url)
        if html_code != "null":
            soup = BeautifulSoup(html_code, 'lxml')
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and re.search(value, script.string):
                    print(f"[Parser]: Found {type_js} on {url}")
                    self.__output[url] = script.string.strip()

    async def __crawl(self) -> None:
        for url in self.url_list:
            for key in self.self_scripts:
                await asyncio.to_thread(self.__found_self_scripts, key, self.self_scripts[key], url)

    def start_crawler(self):
        asyncio.run(self.__crawl())
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(self.__output, f, ensure_ascii=False, indent=4)
