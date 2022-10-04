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

class targetApi:

    def __init__(self, link, filename):
        self.start_offset = 0
        self.cat_page = '/c/{}'
        self.best_selling_rank = 0
        self.folder = 'output'
        self.filename = os.path.join(self.folder, filename)
        self.link = link

    def _requests(self, url):
        headers = {
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
        cookies = {
            'TealeafAkaSid': 'Da5AV3noQszxoVSX1BBvJ11HkNeruGEC',
            'visitorId': '01836E4974590201ACA02C25A0200A09',
            'sapphire': '1',
            'UserLocation': '44601|27.700|85.310|BA|NP',
            'usprivacy': '1YY-',
            'fiatsCookie': 'DSI_794|DSN_Canton|DSZ_44720',
            'ci_pixmgr': 'other',
            'crl8.fpcuid': '6e16c00f-c7cd-4fa9-8f48-6daa78fbf2eb',
            'egsSessionId': '0e8a035e-fe77-42d6-a67e-9d14c75531d4',
            'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJiNmJhNDNjYS1hNTY2LTQzZTEtOTExNi0wOWYwNjJjNDI4MTUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NjQ5ODQ0NDUsImlhdCI6MTY2NDg5ODA0NSwianRpIjoiVEdULmIyNDljZWZlNGFlZDQ0MDhiYmVlMGRkMzZjYTJlZTJkLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjRkM2U3NjFhZTRhMWZjMGUwNjBiMTY1N2NjMjU1Zjg1NjMyMzU5OGRmYzlkOThjODY0OTViMTA2NGYyNzAwMTciLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.ZYz9I5k7yymC5-Jqq3If2K3bUtm7sIi70uKpvqDhHKHv1KfuB8-Qt1Q-UWwUIBdGJUwUnY5WRLy8sg7s-eZmo7t6h_oQGiYLmnnVZm6N2PIPtBHKO13B4T7KyMblO4KFqze7C9_L_DOgegHDL0Ao2e6ZjiueZxOxDzZP63R2j7C1T8QU2TBkTR0-ycij3I4Sk6rtmNuNXukJrsdIT09aPfZ3cBEyMDO49vUHUAfpNzhX7A26EfLv_Ce0zAPojNQdC-MPRtDdxEnq1kSf1NkyUIxnU4Ne3cuhZHOdoLNYZaXWrtsxH7v6MZBRzaWtYLaAya26W2DRwaKMycnb1eu7Ow',
            'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiJiNmJhNDNjYS1hNTY2LTQzZTEtOTExNi0wOWYwNjJjNDI4MTUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NjQ5ODQ0NDUsImlhdCI6MTY2NDg5ODA0NSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.',
            'refreshToken': 'pbrDqasvmejsGhWzpM8sNMjgQ3xwRvWMc27tFIyxEO_HcHMc6CTYQavuMXfN1g2GsoKl6x5xzuK8fnvI1wZYsw',
            'ffsession': '{%22sessionHash%22:%2210e9b3c1f09c1b1664002654784%22%2C%22prevPageName%22:%22home:%20bath:%20beach%20towels%22%2C%22prevPageType%22:%22level%203%22%2C%22prevPageUrl%22:%22https://www.target.com/c/beach-towels-bath-home/red/-/N-5xtv6?sortBy=bestselling&moveTo=product-list-grid%22%2C%22prevSearchTerm%22:%22non-search%22%2C%22sessionHit%22:18}',
            '_mitata': 'MmE3YjVjMDgzZWU1OThkN2YzYTdiMTYzMTBhZDQzYmEwZDA3OGEzNWE3NjE1NmVlYmQ0MWNhMDZhMjkxOTM4Nw==_/@#/1664898277_/@#/cOaP4hamOE7aXwla_/@#/NjIwNTg4YWE2ZDNkMGVhNjJjZWQzMWFlNjAwOGY1Yzg2NzA1MDJjZWNmNmNjMDk1MWY1MWE3MTdjMDE0NTA3Mg==_/@#/000',
        }
        while True:
            try:
                response = requests.get(url, headers=headers, cookies=cookies)
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
        response = self._requests(url)
        data = json.loads(response.text).get('data').get('search')
        results = data.get('products')
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
            fabric_type = self.get_fabric_type(highlight_for_attr)
            title = result.get('item').get('product_description').get('title')
            try:
                title = unidecode(title).replace('&#34;','\"')
            except:
                pass
            product_type = self.get_product_type(title)
            sale_price = result.get('price').get('formatted_current_price')
            list_price = result.get('price').get('formatted_comparison_price')
            if list_price is None:
                list_price = sale_price
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
            except:
                ribbons = []
            available_colors = []
            best_selling_color = ''
            try:
                colors = self.get_swatches(result, 'Color')
                for color in colors:
                    if tcin in color:
                        best_selling_color = color[1]
                    else:
                        available_colors.append(color[1])
            except:
                pass
            for ac in available_colors:
                if ac in list(self.colors_frequency.keys()):
                    self.colors_frequency[ac] += 1
                else:
                    self.colors_frequency[ac] = 1
            available_sizes = []
            best_selling_size = ''
            try:
                sizes = self.get_swatches(result, 'Size')
                for size in sizes:
                    if tcin in size:
                        best_selling_size = size[1]
                    else:
                        available_sizes.append(size[1])
            except:
                pass
            pieces = self.get_description(result, 'Pieces')
            piece1 = self.get_description(result, 'Piece 1')
            fabric_name = self.get_description(result, 'Fabric Name')
            textile_material = self.get_description(result, 'Textile Material')
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
                'Crawling Time': crawling_time,
                'Best Selling Rank': self.best_selling_rank,
                'Product Url': product_url,
                'Category': 'Bath Towels',
                'Name': title,
                'Brand': brand,
                'Material': material,
                'Pattern': pattern,
                'Highlights 1': highlight[1],
                'Highlights 2': highlight[2],
                'Highlights 3': highlight[3],
                'Highlights 4': highlight[4],
                'Highlights 5': highlight[5],
                'Best Selling Size': best_selling_size,
                'Available size': available_sizes,
                'Best Selling color': best_selling_color,
                'Available color': available_colors,
                'Overall star rating': rating,
                'Total Number Reviews': review_count,
                'Value': value,
                'Quality': quality,
                'Total Star Ratings': rating_count,
                'Star1 count': distribution['1'],
                'Star2 count': distribution['2'],
                'Star3 count': distribution['3'],
                'Star4 count': distribution['4'],
                'Star5 count': distribution['5'],
                'List Price': list_price,
                'Sale Price': sale_price,
                'No of pieces': pieces,
                'Piece 1': piece1,
                'Fabric Name': fabric_name,
                'Textile_material': textile_material,
                'Style': style,
                'Protective Qualities': protective_qualities,
                'Fabric_weight_type': fabric_weight_type,
                'Ribbons': ribbons,
                'Product Type': product_type,
                'Attribute': attributes,
                'Pattern New': pattern_new,
                'Fabric Type': fabric_type,
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
        # url = 'https://www.target.com/c/bath-towels-home/-/N-5xtv9?sortBy=newest&moveTo=product-list-grid'
        link = self.link
        while more:
            more = self.get_products(link, start)
            start += 24
        print(f'[green][+][/green] Task completed successfully.')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Script to scrape product details for target.com', epilog='Output are saved inside output folder.')
    parser.add_argument('-o','--output', type=str, help='Enter output filename with extension. eg. output.csv', default='output.csv')
    parser.add_argument('-u', '--url', type=str, help='Enter grid url for target website. Note: put url inside quote.')
    args = parser.parse_args()
    tg = targetApi(args.url, args.output)
    tg.main()
