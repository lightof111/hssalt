
# Overview

This is a python tool that downloads the html pages from the "28947-group-therapy-need-to-blow-off-steam-mega-salty" thread and saves the comments as json files in the format: comment, commentid, commentDate.

This uses BeautifulSoup and lxml to parse the HTML pages

To run: 
make sure you have lxml and BeautifulSoup installed
python -i scraper.py will let you run in interactive mode. download will download pages a through b and save them in your ./comments folder. reload will load pages a through b from your ./comments folder into memory.

