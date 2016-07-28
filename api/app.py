#!/usr/bin/env python
from flask import Flask, jsonify, json
from uuid import uuid4 as uuid
import os

app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

config_datafile = open(os.path.join(SITE_ROOT, 'config.json'))
config = json.load(config_datafile)

app_prefix = u''
if 'prefix' in config:
	app_prefix = config['prefix']

top_methods = {
	'methods': [
		{
			'name': u'getWords',
			'url': app_prefix + u'/api/v1/words',
			'method': u'GET'
		}
	]
}

words_datafile = open(os.path.join(SITE_ROOT, 'data', 'words.json'))
words = json.load(words_datafile)

if not 'words' in words:
	words['words'] = []

for o in words['words']:
	if not 'id' in o:
		o.id = str(uuid())

@app.route(app_prefix + '/api/v1')
def index():
	return jsonify(top_methods)

@app.route(app_prefix + '/api/v1/words', methods=['GET'])
def get_words():
	return jsonify(words)


if __name__ == '__main__':
	app.run(debug=True)

