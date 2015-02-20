#!/bin/bash
~/src/tiebabot/.venv/bin/python ~/src/tiebabot/tiebabot/main.py
cp -r -v  ~/src/tiebabot/tiebabot/templates/css  /var/www/tieba/
cp -r -v  ~/src/tiebabot/tiebabot/templates/js  /var/www/tieba/
