#!/usr/bin/env python
from flask import Flask, jsonify, json, abort, make_response, request
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
		},
		{
			'name': u'addWord',
			'url': app_prefix + u'/api/v1/words',
			'method': u'POST'
		}
	]
}

words_datafile = open(os.path.join(SITE_ROOT, 'data', 'words.json'))
words = json.load(words_datafile)
words_datafile.close()

def flush_data():
	words_datafile = open(os.path.join(SITE_ROOT, 'data', 'words.json'), 'w')
	json.dump(words, words_datafile)
	words_datafile.close()	

if not 'words' in words:
	words['words'] = []

for o in words['words']:
	if not 'id' in o:
		o.id = str(uuid())

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'not found'}), 404)

@app.route(app_prefix + '/api/v1')
def index():
	return jsonify(top_methods)

@app.route(app_prefix + '/api/v1/words', methods=['GET'])
def get_words():
	return jsonify(words)

@app.route(app_prefix + '/api/v1/words/<int:word_id>', methods=['GET'])
def get_word(word_id):
	word = [word for word in words if word['id'] == word_id]
	if len(word) == 0:
		abort(404)
	return jsonify({'word': word[0]})

@app.route(app_prefix + '/api/v1/words', methods=['POST'])
def add_word():
	if not request.json or not 'word' in request.json:
		print request.json
		abort(400)
	word = {
		'id': str(uuid()),
		'word': request.json['word']
	}
	words['words'].append(word)
	flush_data()
	return jsonify({'word': word}), 201

if __name__ == '__main__':
	app.run(debug=True)

