import requests
from bs4 import BeautifulSoup

class targetApi:

    def __init__(self) -> None:
        pass

    def _requests(self, url):
        response = requests.get(url)
        return response

    def _soup(self, response):
        return BeautifulSoup(response.text, 'html.parser')

    def main(self):
        url = 'https://www.target.com/c/bath-towels-home/-/N-5xtv9?sortBy=newest&moveTo=product-list-grid'

        
        params = {
            'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
            'category': '5xtv9',
            'channel': 'WEB',
            'count': '24',
            'default_purchasability_filter': 'true',
            'offset': self.start_offset,
            'page': '/c/5xtv9',
            'platform': 'desktop',
            'pricing_store_id': '794',
            'sort_by': 'newest',
            'store_ids': '794,2346,2044,793,2119',
            'useragent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'visitor_id': '01836E4974590201ACA02C25A0200A09',
            'zip': '44601',
        }
        pass

if __name__=='__main__':
    tg = targetApi()
    tg.main()