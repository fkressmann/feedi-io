#!/usr/bin/env bash

flask db upgrade
exec gunicorn -b :8080 app:app