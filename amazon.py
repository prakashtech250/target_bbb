import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from rich import print
import json, os, csv, argparse, re, random

class AmazonApi:
    def __init__(self, filename='output.csv'):
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.6',
            'Connection': 'keep-alive',
            'Origin': 'https://www.amazon.com',
            'Referer': 'https://www.amazon.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        self.user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20190101 Firefox/70.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        ]
        self.API = ''
        self.base_url = 'https://www.amazon.com'
        self.rank = 0
        self.cookies = self.cookiesToDict('cookies/amazon_cookies.json')
        self.folder = 'output'
        self.filename = os.path.join(self.folder, filename)
        self.designList = ['Cabana Stripe', 'Stripe','Jacquard', 'Peshtemal', 'Printed', 'Solid', 'Floral', 'Nautical', 'Geometric']

    def cookiesToDict(self, filename):
        print("[green][+][/green] Getting cookies from [u]amazon_cookies.json[/u]")
        data = None
        cookies = {}
        try:
            with open(filename,"r") as f:
                data = json.load(f)
        except Exception as e:
            print("[red][-] [u]amazon_cookies.json[/u] not found in the path[/red]")
            return None
        
        try:
            for i in data:
                cookies[i['name']] = i['value']
        except Exception as e:
            print("[red][-] Cookies are not in proper format[/red]")
            return None

        return cookies 

    def write_csv(self, data, mode):
        with open(self.filename, mode, newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(data)


    def save_data(self,data):
        if os.path.exists(self.folder):
            pass
        else:
            os.mkdir(self.folder)
        rows = list(data.values())
        title = list(data.keys())
        if os.path.exists(self.filename):
            self.write_csv(rows, 'a')
        else:
            self.write_csv(title, 'w')
            self.write_csv(rows, 'a')

    def _requests(self, url):
        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        while True:
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies)
                break
            except Exception as e:
                print(f'[red][-][/red] Error: {e}')
        return response

    def _soup(self, response):
        return BeautifulSoup(response.text, 'html.parser')

    def _time_now(self):
        now = datetime.now()
        crawling_time = now.strftime("%Y/%m/%d %H:%M:%S")
        return crawling_time

    def get_products(self, url):
        response = self._requests(url)
        soup = self._soup(response)
        test = soup.find(class_="p13n-desktop-grid").get('data-client-recs-list')
        json_data = json.loads(test)
        for ji, jd in enumerate(json_data):
            asin = jd.get('id')
            product_url = 'https://www.amazon.com/dp/' + asin
            self.get_details(product_url)

    def get_features(self,asin):
        url = 'https://www.amazon.in/hz/reviews-render/ajax/lazy-widgets/stream?asin={}&csrf=gpiBcGvSxAwt24MiRKAPH9bY%2FefoS5ELeFZdAf4AAAABAAAAAGJVqjxyYXcAAAAA%2B4kUEk%2F7iMGR3xPcX6iU&language=en_IN&lazyWidget=cr-summarization-attributes'.format(asin)
        url = f'https://www.amazon.com/hz/reviews-render/ajax/lazy-widgets/stream?asin={asin}&csrf=hPpplffoBZtowHO1MMb0krftmSqS9kx6ktt%2B7ja1zBfwAAAAAGM%2B6UcAAAAB&language=en_US&lazyWidget=cr-summarization-attributes'
        response = self._requests(url)
        regex = '(?<=\[)(.*)(?=])'
        inside_brackets = re.search(regex, response.text).group(0)
        html_format = inside_brackets.split(',')[2].replace('\\"','"').replace('\\n','')
        soup = BeautifulSoup(html_format, 'html.parser')
        light_weight_div = soup.find(id='cr-summarization-attribute-attr-light-weight')
        if light_weight_div:
            light_weight = light_weight_div.find(class_='a-color-tertiary').text.strip()
        else:
            light_weight = None
        softness_div = soup.find(id='cr-summarization-attribute-attr-softness')
        if softness_div:
            softness = softness_div.find(class_='a-color-tertiary').text.strip()
        else:
            softness = None
        absorbency_div = soup.find(id='cr-summarization-attribute-attr-absorbency')
        if absorbency_div:
            absorbency = absorbency_div.find(class_='a-color-tertiary').text.strip()
        else:
            absorbency = None
        value_div = soup.find(id='cr-summarization-attribute-attr-value')
        if value_div:
            value = value_div.find(class_='a-color-tertiary').text.strip()
        else:
            value = None
        travel_div = soup.find(id='cr-summarization-attribute-attr-for-travel')
        if travel_div:
            travel = travel_div.find(class_='a-color-tertiary').text.strip()
        else:
            travel = None
        durability_div = soup.find(id='cr-summarization-attribute-attr-durability')
        if durability_div:
            durability = durability_div.find(class_='a-color-tertiary').text.strip()
        else:
            durability = None
        easy_clean_div = soup.find(id='cr-summarization-attribute-attr-easy-to-clean')
        if easy_clean_div:
            easy_clean = easy_clean_div.find(class_='a-color-tertiary').text.strip()
        else:
            easy_clean = None
        features = (light_weight, softness, absorbency, value, travel, durability, easy_clean)
        return features

    def get_details(self, url):
        supplier = None
        color = None
        all_colors = None
        blend = None
        pack = None
        size = None
        gsm = None
        twlCat = None
        design = None
        kidAdult = None
        price = None
        discount = None
        title = None
        pattern = None
        reviews = None
        first_available = None
        self.rank += 1
        print(f'[green][+][/green] {self.rank}: {url} [Collecting]', end='\r')
        response = self._requests(url)
        soup = self._soup(response)
        try:
            asin = soup.find(id="ASIN").get('value')
        except:
            asin = url.split('/')[-1]
        price_whole = soup.find(class_='a-price-whole')
        price_fraction = soup.find(class_="a-price-fraction")
        sns_price = soup.find(id="sns-base-price")
        if price_whole and price_fraction:
            price = f'{price_whole.get_text()}{price_fraction.get_text()}'
        elif price_whole:
            price = price_whole.get_text()
        elif sns_price:
            price = sns_price.get_text()

        try:
            discount = soup.find(class_='savingsPercentage').text.replace('-','')
        except:
            discount = '0%'

        title_div = soup.find(id="productTitle")
        if title_div:
            title = title_div.text.strip()
        else:
            title = None
        if title:
            if 'kids' in title.lower() and 'adults' in title.lower():
                kidAdult = 'Kids/Adults'
            elif 'kid' in title.lower():
                kidAdult = 'Kids'
            elif 'adult' in title.lower():
                kidAdult = 'Adults'
            else:
                kidAdult = ''
        else:
            kidAdult = None
        if title:
            for dl in self.designList:
                if dl.lower() in title.lower():
                    design = dl 
                    break
        pack = 1
        colors_div = soup.find(id="variation_color_name")
        if colors_div:
            color_divs = colors_div.find_all('li')
            colors = [x.img.get('alt') for x in color_divs]
            all_colors = ','.join(colors)
        else:
            all_colors = None
        detailsTable = soup.find(id="productDetails_detailBullets_sections1")
        tableRow = detailsTable.find_all('tr')
        for tr in tableRow:
            heading = tr.th.text.strip()
            detail = tr.td.text.strip()
            if 'Brand' in heading:
                supplier = detail
            if 'Manufacturer' in heading and supplier is None:
                supplier = detail
            if 'Color' in heading:
                color = detail
            if 'Material' in heading:
                blend = detail
            if 'Number of Items' in heading:
                pack = detail.strip()
            if 'Pattern' in heading and pattern is None:
                pattern = detail.strip()
            if 'Dimensions' in heading and size is None:
                size = detail
            # if 'Size' in heading and size is None:
            #     if 'Pack' not in detail:
            #         size = detail
            if 'Weight' in heading:
                gsm = detail.strip()
            if 'Date First Available' in heading:
                first_available = detail.strip()
        
        detailsTable2 = soup.find(id="productOverview_feature_div").table
        tableRow = detailsTable2.find_all('tr')
        for tr in tableRow:
            heading = tr.find_all('td')[0].text.strip()
            detail = tr.find_all('td')[1].text.strip()
            if 'Brand' in heading and supplier is None:
                supplier = detail
            if 'Manufacturer' in heading and supplier is None:
                supplier = detail
            if 'Color' in heading and color is None:
                color = detail
            if 'Material' in heading and blend is None:
                blend = detail
            if 'Number of Pieces' in heading and pack is None:
                pack = detail.strip()
            if 'Number of Items' in heading and pack is None:
                pack = detail.strip()
            if 'Dimensions' in heading and size is None:
                size = detail
            if 'Weight' in heading and gsm is None:
                gsm = detail.strip()
            if 'Pattern' in heading and pattern is None:
                pattern = detail.strip()
        twlCat = str(pack) + ' Beach'
        if color is None:
            color_div = soup.find(id="variation_color_name")
            if color_div:
                color = color_div.find(class_='selection').text.strip()
        if all_colors is None:
            all_colors = color
        # if size:
        #     size = size.replace('inches','').replace('X','*').replace(' ','').replace('in','').replace('x','*').replace('\"','').replace('\'','').replace('Inch','').replace('L','').replace('W','')
        rating_div = soup.find(id="averageCustomerReviews")
        rating = rating_div.find(class_="a-icon-alt").text.split(' ')[0]
        reviews = soup.find(id="acrCustomerReviewText").text.replace('ratings','').replace(',','').strip()
        features = self.get_features(asin)
        # light_weight, softness, absorbency, value, travel, durability, easy_clean
        scraped_items = {
            'Rank': self.rank,
            'ASIN': asin,
            'Title': title,
            'Supplier': supplier,
            'Color': color,
            'Available Colors': all_colors,
            'Blend': blend,
            'Pattern': pattern,
            'Pack Factor': pack,
            'Size (In inches)': size,
            'GSM': gsm,
            'Towel Category': twlCat,
            'Design': design,
            'Adult/Kids': kidAdult,
            'MRP(In $)': price,
            'Discount': discount,
            'Rating': rating,
            'Reviews': reviews,
            'Date First Available': first_available,
            'Light Weight': features[0],
            'Softness': features[1],
            'Absorbency': features[2],
            'Value for Money': features[3],
            'For Traveling': features[4],
            'Durability': features[5],
            'Easy to Clean': features[6],
            'Product Url': url,
        }
        self.save_data(scraped_items)
        print(f'[green][+][/green] {self.rank}: {url} [Saved]       ')

    def main(self):
        url = 'https://www.amazon.com/gp/bestsellers/home-garden/3731751'
        self.get_products(url)
        url = url + '?pg=2'
        self.get_products(url)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Script to scrape product details for amazon.com', epilog='Output are saved inside output folder.')
    parser.add_argument('-o','--output', type=str, help='Enter output filename with extension. eg. output.csv', default='output.csv')
    args = parser.parse_args()
    am = AmazonApi(args.output)
    am.main()

    # am = AmazonApi('test.csv')
    # am.get_features('B09RCCFX1N')
    # am.get_details('https://www.amazon.com/dp/B06XKCF6L8')

