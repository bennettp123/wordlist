#!/bin/bash
cd "$(dirname "$0")"
virtualenv flask
flask/bin/pip install flask

