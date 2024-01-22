import sys
import asyncio
import colorama
from colorama import Fore
from crawler import Crawler
from spider import HtmlParser

colorama.init()

def logo():
    print('       _    ___      __'+Fore.RED+ '_____'+Fore.WHITE) 
    print('      | |  | \ \    / /'+Fore.RED+' ____|'+Fore.WHITE)
    print('      | |__| |\ \  / / '+Fore.RED+'(___  '+Fore.WHITE)
    print('      |  __  | \ \/ / '+Fore.RED+'\___ \ '+Fore.WHITE)
    print('      | |  | |  \  /  '+Fore.RED+'____) |'+Fore.WHITE)
    print('      |_|  |_|   \/  '+Fore.RED+'|_____/ '+Fore.WHITE)
    print('')
    print('  --=='+Fore.RED+'['+Fore.WHITE+'~'+ Fore.RED+']'+Fore.WHITE+' Hello Vuln Script '+Fore.RED+'['+Fore.WHITE+'~'+ Fore.RED+']'+Fore.WHITE+'==-- ')
    print('   --=='+Fore.RED+'['+Fore.WHITE+'~'+ Fore.RED+']'+Fore.WHITE+' Version: 0.1 '+Fore.RED+'['+Fore.WHITE+'~'+ Fore.RED+']'+Fore.WHITE+'==--    ')
    print('')                

def help_view():
    print(Fore.RED + '──────────────────────────────────────────────────────────' + Fore.WHITE)
    print(Fore.RED + '[' + Fore.WHITE + 'Usage' + Fore.RED + ']: ' + Fore.WHITE + 'python3 main.py' + Fore.RED + ' spider '+ Fore.WHITE + 'https://example.com')
    print(Fore.RED + '[' + Fore.WHITE + 'Usage' + Fore.RED + ']: ' + Fore.WHITE + 'python3 main.py' + Fore.RED + ' parse '+ Fore.WHITE + 'urls.txt')
    print(Fore.RED + '──────────────────────────────────────────────────────────' + Fore.WHITE)
    print(Fore.RED + '[' + Fore.WHITE + 'Options' + Fore.RED + ']: ')
    print('\tspider\t'+Fore.WHITE+'Searches for URLs and writes them to a file urls.txt')
    print(Fore.RED + '\tparser\t'+Fore.WHITE+'Based on a regular expression, it searches for scripts from URLs')
    print('')

def main() -> None:
    if len(sys.argv) < 2:
        help_view()
        sys.exit()

    mode = sys.argv[1]
    url_wordlist = sys.argv[2]

    if mode == "spider":
        parser = HtmlParser()
        parser.set_url(url_wordlist)
        asyncio.run(parser.start())

        with open("urls.txt", "w") as f:
            for url in parser.parsed_urls:
                f.write(f"{url}\n")
    elif mode == "parser":
        with open(url_wordlist) as file:
            lines = [line.rstrip() for line in file]
        crawler = Crawler(lines)
        crawler.start_crawler()

if __name__ == "__main__":
    logo()
    main()
