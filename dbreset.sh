#!/bin/bash
# Resets the database

export FLASK_APP=main.py
rm app.db
rm -rf migrations
flask db init
flask db migrate -m "reset db"
flask db upgrade
