#!/bin/bash

echo "gunicorn -b 127.0.0.1:8000 wsgi:application -D"
gunicorn -b 127.0.0.1:8000 wsgi:application -D
