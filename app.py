# -*- coding: utf-8 -*-
import base64
from io import BytesIO
from flask import Flask, request, abort
from PIL import Image
import requests
from settings import API_HOST, API_PORT, API_URL

app = Flask(__name__)


def __save_image(image_name, image_file):
    with open(f'media/{image_name}', 'wb') as out:
        out.write(image_file.read())
    image = Image.open(image_file)
    image.thumbnail((100, 100))
    image.save(f'media/thumb_{image_name}')


@app.route(API_URL, methods=['POST'])
def api():
    if 'application/x-www-form-urlencoded' in request.content_type:
        session = requests.Session()
        session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 '
                                         '(KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
        for image_name, image_url in request.form.items():
            response = session.get(image_url)
            if response.status_code != 200:
                abort(response.status_code)
            __save_image(image_name, BytesIO(response.content))
    if 'application/json' in request.content_type:
        for image_name, image in request.json.items():
            __save_image(image_name, BytesIO(base64.standard_b64decode(image)))
    if 'multipart/form-data' in request.content_type:
        for image_name, image in request.files.items():
            __save_image(image_name, image)
    return 'ok'


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, debug=True)
