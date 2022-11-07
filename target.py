import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlencode
import json
from datetime import datetime
import time
from rich import print
from unidecode import unidecode
import csv
import os
import argparse
import random

class targetApi:

    def __init__(self, link, filename):
        self.start_offset = 0
        self.cat_page = '/c/{}'
        self.best_selling_rank = 0
        self.folder = 'output'
        self.filename = os.path.join(self.folder, filename)
        self.link = link
        self.cookies = self.cookiesToDict('cookies/target_cookies.json')
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
        self.headers = {
            'authority': 'redsky.target.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.6',
            'origin': 'https://www.target.com',
            'referer': 'https://www.target.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }

    def cookiesToDict(self, filename):
        print("[green][+][/green] Getting cookies from [u]target_cookies.json[/u]")
        data = None
        cookies = {}
        try:
            with open(filename,"r") as f:
                data = json.load(f)
        except Exception as e:
            print("[red][-] [u]target_cookies.json[/u] not found in the path[/red]")
            return None
        
        try:
            for i in data:
                cookies[i['name']] = i['value']
        except Exception as e:
            print("[red][-] Cookies are not in proper format[/red]")
            return None

        return cookies

    def _requests(self, url):
        self.headers['User-Agent'] = random.choice(self.user_agent_list)
        while True:
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies)
                break
            except Exception as e:
                print(f'[red][-][/red] Error: {e}')
        return response

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

    def _soup(self, response):
        return BeautifulSoup(response.text, 'html.parser')

    def _time_now(self):
        now = datetime.now()
        crawling_time = now.strftime("%Y/%m/%d %H:%M:%S")
        return crawling_time

    def get_param_value(self, url):
        cat_id_path = r'(?=N-)(.*)'
        sortBy_path = r'(?=sortBy=)(.*)(?=\&)'
        cat_id = re.search(cat_id_path, url.split('?')[0]).group(0).replace('N-','')
        sortBy = re.search(sortBy_path, url.split('?')[1]).group(0).split('=')[1]
        return cat_id, sortBy

    def get_attribute(self, highlights):
        output_attributes = list()
        list_of_attribute = ['absorbent','Fade-resistant','Low-lint','soft','soft plush','Plush','Super soft and absorbent','soft and absorbent']
        for la in list_of_attribute:
            if la.lower() in highlights.lower():
                output_attributes.append(la)
        if len(output_attributes) > 1:
            for oi, oa in enumerate(output_attributes):
                try:
                    if oa in output_attributes[oi+1]:
                        output_attributes.remove(oa)
                except:
                    pass
        return output_attributes

    def get_pattern_new(self, highlights):
        output_attributes = list()
        list_of_attribute = ['Solid','Printed','Embroidered','Jacquard','Striped','Decorative Embroidery']
        for la in list_of_attribute:
            if la.lower() in highlights.lower():
                output_attributes.append(la)
        if len(output_attributes) > 1:
            for oi, oa in enumerate(output_attributes):
                try:
                    if oa in output_attributes[oi+1]:
                        output_attributes.remove(oa)
                except:
                    pass
        return output_attributes

    def get_fabric_type(self, highlights):
        output_attributes = list()
        list_of_attribute = ['Turkish','Organic','Modal','Recycled','Pima','Supima','Egyptian']
        for la in list_of_attribute:
            if la.lower() in highlights.lower():
                output_attributes.append(la)
        if len(output_attributes) > 1:
            for oi, oa in enumerate(output_attributes):
                try:
                    if oa in output_attributes[oi+1]:
                        output_attributes.remove(oa)
                except:
                    pass
        return output_attributes

    def get_product_type(self, title):
        output_type = list()
        list_of_type = ['Bath Towel','Bath Towel Set','Hand Towel','Hand Towel Set','Washcloth' ,'Washcloth Set','Bathrobe', 'Wrap', 'Robe', 'Bathrobe']
        for lt in list_of_type:
            if lt.lower() in title.lower():
                output_type.append(lt)
        if len(output_type) > 1:
            for oi,ot in enumerate(output_type):
                try:
                    if ot in output_type[oi+1]:
                        output_type.remove(ot)
                except:
                    pass
        return output_type

    def get_description(self, result, input_string):
        data = result.get('item').get('product_description').get('bullet_descriptions')
        if data:
            for d in data:
                if input_string in d:
                    output_str = d.split(':')[1:]
                    output_str = ' '.join(output_str)
                    output_str = output_str.replace('</B>','').strip()
                    break
                else:
                    output_str = None
        else:
            output_str = None
        return output_str

    def get_ratings_and_reviews(self, tcin):
        url = f'https://r2d2.target.com/ggc/v2/summary?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&hasOnlyPhotos=false&includes=statistics&page=0&entity=&ratingFilter=&reviewedId={tcin}&reviewType=PRODUCT&verifiedOnly=false'
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    break
            except:
                time.sleep(2)
        value = ''
        quality = ''
        if response.status_code == 200:
            json_data = json.loads(response.text)
            result = json_data['statistics']
            review_count = result.get('review_count')
            average_rating = result.get('rating').get('average')
            total_rating = result.get('rating').get('count')
            averages = result.get('rating').get('secondary_averages')
            for average in averages:
                if average.get('label') == 'quality':
                    quality = average.get('value')
                if average.get('label') == 'value':
                    value = average.get('value')
            distribution = result.get('rating').get('distribution')
        return review_count, average_rating, total_rating, quality, value, distribution

    def check_features(self, feature, title, highlight_for_attr):
        if feature in title.lower():
            return 1
        elif feature in highlight_for_attr.lower():
            return 1
        else:
            return 0

    def get_swatches(self,result, title, tcin):
        try:
            themes = result['parent']['variation_summary']['themes']
        except:
            themes = None
        swatch = None
        swatches = []
        best_selling = None
        if themes:
            for theme in themes:
                if title == theme['name'].lower():
                    swatchList = theme['swatches']
                    for sw in swatchList:
                        swatchValue = sw['value']
                        swatches.append(swatchValue)
                        if tcin == sw['first_child']['tcin']:
                            best_selling = swatchValue
        if swatches:
            swatch = ', '.join(swatches)
        return swatch, best_selling

    def get_pack(self, title):
        pack = None
        for i in range(1, 10):
            pack1 = f'{i}-pack'
            pack2 = f'{i}pk'
            pack3 = f'{i} pack'
            if pack1 in title.lower() or pack2 in title.lower() or pack3 in title.lower():
                pack = i
                break
        return pack

    def get_products(self, params_url, start):
        main_url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1?'
        cat_id, sort_by = self.get_param_value(params_url)
        cat_page = f'/c/{cat_id}'
        params = {
            'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
            'category': '',
            'channel': 'WEB',
            'count': '24',
            'default_purchasability_filter': 'true',
            'offset': start,
            'page': '',
            'platform': 'desktop',
            'pricing_store_id': '794',
            'sort_by': '',
            'store_ids': '794,2346,2044,793,2119',
            'useragent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'visitor_id': '01836E4974590201ACA02C25A0200A09',
            'zip': '44601',
        }
        params['category'] = cat_id.strip()
        params['page'] = cat_page.strip()
        params['sort_by'] = sort_by.strip()

        url = main_url + urlencode(params)
        while True:
            response = self._requests(url)
            try:   
                data = json.loads(response.text).get('data').get('search')
                results = data.get('products')
                break
            except:
                print(response.text)
                for i in range(10):
                    print(f'There is an error...Script will try again in {10-i}  ', end='\r')
                    time.sleep(1)
                self.cookies = self.cookiesToDict('cookies/target_cookies.json')
        total_results = data.get('search_response').get('typed_metadata').get('total_results')
        try:
            colorList = self.get_facet_list(data, 'd_color_all')
        except:
            colorList = []
        for cL in colorList:
            if cL not in list(self.colors_frequency.keys()):
                self.colors_frequency[cL] = 0
        try:
            materialList = self.get_facet_list(data, 'd_throwpillow_covermaterial')
        except:
            materialList = ['1']
        for result in results:
            self.best_selling_rank += 1
            product_url = result.get('item').get('enrichment').get('buy_url')
            category = ''
            highlight = {
            1: '',
            2: '',
            3: '',
            4: '',
            5: ''
            }
            try:
                highlights = result.get('item').get('product_description').get('soft_bullets').get('bullets')
                for i, hl in enumerate(highlights):
                    highlight[i+1] = hl
            except:
                pass
            highlight_for_attr = highlight[1] + highlight[2] + highlight[3] + highlight[4] + highlight[5]
            attributes = self.get_attribute(highlight_for_attr)
            pattern_new = self.get_pattern_new(highlight_for_attr)
            pattern_new = ', '.join(pattern_new)
            fabric_type = self.get_fabric_type(highlight_for_attr)
            title = result.get('item').get('product_description').get('title')
            try:
                title = unidecode(title).replace('&#34;','\"')
            except:
                pass
            product_type = self.get_product_type(title)
            product_type = ', '.join(product_type)
            sale_price = result.get('price').get('formatted_current_price').replace('$','')
            list_price = result.get('price').get('formatted_comparison_price')
            if list_price is None:
                list_price = sale_price
            else:
                list_price = list_price.replace('$','')
            try:
                discount = (float(list_price) - float(sale_price)) / float(list_price)
                discount_per = discount * 100
            except:
                discount_per = None
            try:
                materials = self.get_description(result, "Material")
            except:
                materials = None
            material = []
            if materials is not None:
                for ml in materialList:
                    if ml in materials:
                        material.append(ml)
            try:
                pattern = self.get_description(result, "Pattern")
            except:
                pattern = None
            try:
                thread_count = self.get_description(result, "Thread Count")
            except:
                thread_count = ''
            try:
                brand = result.get('item').get('primary_brand').get('name')
            except:
                brand = ''
            try:
                includes = self.get_description(result,'Includes')
            except:
                includes = None
            try:
                depth = self.get_description(result, 'Fits Mattress Depth')
            except:
                depth = None
            try:
                size = self.get_description(result, 'Size')
            except:
                size = None

            tcin = result.get('tcin')
            try:
                ribbons = result.get('parent').get('item').get('ribbons')
                ribbons = ', '.join(ribbons)
            except:
                ribbons = None

            available_color, best_selling_color = self.get_swatches(result, 'color', tcin)
            available_size, best_selling_size = self.get_swatches(result, 'size', tcin)

            pieces = self.get_description(result, 'Pieces')
            piece1 = self.get_description(result, 'Piece 1')
            fabric_name = self.get_description(result, 'Fabric Name')
            textile_material = self.get_description(result, 'Textile Material')
            dimensions = self.get_description(result, 'Dimensions')
            style = self.get_description(result,'Style')
            protective_qualities = self.get_description(result, 'Care and Cleaning')
            fabric_weight_type = self.get_description(result, 'Fabric Weight Type')
            if pieces is not None:
                pieces = pieces.replace('</B>','').strip()
            try:
                weight_type = self.get_description(result, 'Fabric Weight Type').replace('</B>','').strip()
            except:
                weight_type = ''
            try:
                care = self.description(result, 'Care and Cleaning')
            except: 
                care = ''
            review_count, rating, rating_count, quality, value, distribution = self.get_ratings_and_reviews(tcin)
            crawling_time = self._time_now()
            data = {
                'Best Selling Rank': self.best_selling_rank,
                'Title': title,
                'Brand': brand,
                'Highlights 1': highlight[1],
                'Highlights 2': highlight[2],
                'Highlights 3': highlight[3],
                'Highlights 4': highlight[4],
                'Highlights 5': highlight[5],
                'Size': available_size,
                'Pack': self.get_pack(title),
                'Best Selling color': best_selling_color,
                'Available color': available_color,
                'Overall star rating': rating,
                'Total Number Reviews': review_count,
                'List Price': list_price,
                'Sale Price': sale_price,
                'Discount %': discount_per,
                'No of pieces': pieces,
                'Dimensions': dimensions,
                'Fabric Name': fabric_name,
                'Textile_material': textile_material,
                'Fabric_weight_type': fabric_weight_type,
                'Ribbons': ribbons,
                'Product Type': product_type,
                'Pattern New': pattern_new,
                'Cabana': self.check_features('cabana', title, highlight_for_attr),
                'Sand': self.check_features('sand', title, highlight_for_attr),
                'Pestemal': self.check_features('pestemal', title, highlight_for_attr),
                'Jacquard': self.check_features('jacquard', title, highlight_for_attr),
                'Stripe/Striped': self.check_features('stripe', title, highlight_for_attr),
                'Printed': self.check_features('printed', title, highlight_for_attr),
                'Solid': self.check_features('solid', title, highlight_for_attr),
                'Tie Dye': self.check_features('tie dye', title, highlight_for_attr),
                'Quick Dry': self.check_features('quick dry', title, highlight_for_attr),
                'Oversized': self.check_features('oversize', title, highlight_for_attr),
                'Floral/Flower': self.check_features('floral', title, highlight_for_attr) or self.check_features('flower', title, highlight_for_attr),
                'Adult': self.check_features('adult', title, highlight_for_attr),
                'Kids': self.check_features('kids', title, highlight_for_attr),
                'Product Url': product_url,

                # 'Material': material,
                # 'Available size': available_sizes,
                # 'Value': value,
                # 'Quality': quality,
                # 'Total Star Ratings': rating_count,
                # 'Star1 count': distribution['1'],
                # 'Star2 count': distribution['2'],
                # 'Star3 count': distribution['3'],
                # 'Star4 count': distribution['4'],
                # 'Star5 count': distribution['5'],
                # 'Piece 1': piece1,
                # 'Style': style,
                # 'Protective Qualities': protective_qualities,
                # 'Attribute': attributes,
                # 'Fabric Type': fabric_type,
            }

            self.save_data(data)
            print(f'[green][+][/green] {self.best_selling_rank}: {title}')
        if start < total_results:
            more = True
        else:
            more = False
        return more

    def main(self):
        start = 0
        more = True
        # url = 'https://www.target.com/c/beach-towels-bath-home/red/-/N-5xtv6?sortBy=bestselling&moveTo=product-list-grid'
        url = self.link
        while more:
            more = self.get_products(url, start)
            start += 24
        print(f'[green][+][/green] Task completed successfully.')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Script to scrape product details for target.com', epilog='Output are saved inside output folder.')
    parser.add_argument('-o','--output', type=str, help='Enter output filename with extension. eg. output.csv', default='output.csv')
    parser.add_argument('-u', '--url', type=str, help='Enter grid url for target website. Note: put url inside quote.')
    args = parser.parse_args()
    tg = targetApi(args.url, args.output)
    tg.main()
