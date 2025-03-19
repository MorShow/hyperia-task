from parser import Parser

import json
import unittest
from unittest.mock import patch


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser('test_output.json')

        with patch.object(self.parser, 'get_html',
                          return_value=open('snapshot.html', 'r', encoding='utf-8')):
            self.parser.process()
            self.parser.jsonify()

    def test_count(self):
        with open('test_output.json', 'r', encoding='utf-8') as f:
            self.assertEqual(len(json.load(f)), 14)

    def test_last_json(self):
        with open('test_output.json', 'r', encoding='utf-8') as f:
            obj = json.load(f)
            last_flyer = obj[-1]

            self.assertEqual(last_flyer['shop_name'], 'Marktkauf')
            self.assertEqual(last_flyer['valid_from'], '2025-03-16')
            self.assertEqual(last_flyer['thumbnail'],
                             'https://media.marktjagd.com/16622587_240x339_fillFFFFFF.jpg')

    def test_first_list(self):
        self.assertEqual(self.parser.get_flyers()[0]['shop_name'], 'Kaufland')


if __name__ == '__main__':
    unittest.main()
