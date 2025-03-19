import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class Parser:

    def __init__(self, output_file, url=None):
        # The link might be changed over time, so there is an ability to set it
        self._url = url or 'https://www.prospektmaschine.de/hypermarkte/'
        self._output_file = output_file
        self._flyers = []

    def set_output_file(self, output_file):
        self._output_file = output_file

    def set_url(self, url):
        self._url = url

    def get_url(self):
        return self._url

    def get_html(self):
        try:
            return requests.get(self._url, timeout=30).text
        except requests.exceptions.Timeout:
            print('timeout')
            return ''

    def get_flyers(self):
        return self._flyers

    def process(self):
        self._flyers.clear()

        try:
            soup = BeautifulSoup(self.get_html(), 'lxml')
        except requests.exceptions.MissingSchema:
            print('Invalid web page or html file')
            return

        flyers = soup.find_all('div', class_='brochure-thumb')

        for flyer in flyers:
            info = {}

            info['title'] = flyer.find('p', class_='grid-item-content').text
            info['thumbnail'] = (flyer.find('div', class_='img-container').img.get('src') or
                                 flyer.find('div', class_='img-container').img.get('data-src'))

            shop_url = flyer.a.get('href')
            shop_name = shop_url.split('/')[1].capitalize()
            info['shop_name'] = shop_name

            dates = flyer.find('small', class_='visible-sm').text.split('-')
            dates = [date.strip() for date in dates]
            if len(dates) == 1:
                date1 = datetime.strptime(dates[0].split()[-1], '%d.%m.%Y')
                # The date 'valid_to' could be set to some constant value,
                # but I`ve decided to set the actual time
                date2 = datetime.now()
            else:
                year = dates[1].split('.')[-1]

                dates[0] += year
                date1 = datetime.strptime(dates[0], '%d.%m.%Y')
                date2 = datetime.strptime(dates[1], '%d.%m.%Y')

            info['valid_from'] = date1.strftime('%Y-%m-%d')
            info['valid_to'] = date2.strftime('%Y-%m-%d')
            info['parsed_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self._flyers.append(info)

    def jsonify(self):
        with open(self._output_file, 'w', encoding='utf-8') as f:
            json.dump(self._flyers, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = Parser('output.json')
    parser.process()
    parser.jsonify()
