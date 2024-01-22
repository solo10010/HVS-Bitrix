import requests
import asyncio
from bs4 import BeautifulSoup

class HtmlParser:
    def __init__(self):
        self.__user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        self.parsed_urls = []
        self.url = ""

    def set_url(self, url: str):
        self.url = url

    def __get_html_code(self, url: str):
        try:
            response = requests.get(url, headers={"user-agent": self.__user_agent})
            response.raise_for_status()
            if 'html' in response.headers['content-type']:
                return response.text
            else :
                return "null"
        except requests.RequestException as e:
            print(f"Cannot parse url: {url}, Error: {e}")
            return "null"

    def __extract_dir(self, html_code: str):
        if html_code != "null":
            soup = BeautifulSoup(html_code, 'lxml')
            for tag in soup.find_all(['a', 'form'], href=True):
                href = tag['href']
                if not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '//')):
                    href = "/" + href if not href.startswith("/") else href
                    full_url = f"{self.url}{href}"
                    if full_url not in self.parsed_urls:
                        print(f"[Spider]: {full_url}")
                        self.parsed_urls.append(full_url)

    async def start(self):
        html_code = self.__get_html_code(self.url)
        if html_code != "null":
            self.__extract_dir(html_code)
            for parsed_url in self.parsed_urls:
                new_html_code = self.__get_html_code(parsed_url)
                await asyncio.to_thread(self.__extract_dir, new_html_code)
