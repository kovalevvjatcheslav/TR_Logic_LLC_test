# -*- coding: utf-8 -*-
import os
import base64
import unittest
from hashlib import sha256
from contextlib import ExitStack
import requests
from settings import API_URL, API_HOST, API_PORT


class TestAPI(unittest.TestCase):
    def setUp(self):
        for each in os.listdir('media'):
            os.remove(f'media/{each}')

    def test_multipart_upload(self):
        with ExitStack() as stack:
            files = {image: stack.enter_context(open(f'test_images/{image}', 'rb'))
                     for image in os.listdir('test_images')}
            response = requests.post(f'http://{API_HOST}:{API_PORT}{API_URL}', files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'ok')
        self.__check_files_equality()

    def test_json_upload(self):
        files = {}
        for image_name in os.listdir('test_images'):
            with open(f'test_images/{image_name}', 'rb') as image:
                files.update({image_name: base64.standard_b64encode(image.read()).decode('utf-8')})
        response = requests.post(f'http://{API_HOST}:{API_PORT}{API_URL}', json=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'ok')
        self.__check_files_equality()

    def test_urls_upload(self):
        urls = ('https://i.vimeocdn.com/portrait/58832_300x300.jpg',
                'https://nccscurriculum.org/wp-content/uploads/2015/02/test-button.jpg',
                'http://d.stockcharts.com/img/articles/2016/09/1472786123370392406734.gif')
        files = {url.split('/')[-1]: url for url in urls}
        response = requests.post(f'http://{API_HOST}:{API_PORT}{API_URL}', data=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'ok')

    def __check_files_equality(self):
        for each in os.listdir('test_images'):
            with ExitStack() as stack:
                media_image = stack.enter_context(open(f'media/{each}', 'rb'))
                test_image = stack.enter_context(open(f'test_images/{each}', 'rb'))
                self.assertEqual(sha256(media_image.read()).digest(), sha256(test_image.read()).digest(), msg=each)


if __name__ == '__main__':
    unittest.main()
