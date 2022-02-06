# Install dependecies
# python3 -m pip install --upgrade matplotlib

from PIL import Image, ImageDraw
import urllib.request, json
import sys
import requests
import matplotlib.pyplot as plt
import numpy as np
import calendar
import datetime

# OpenSea collection slug
os_slug = sys.argv[1]

# OpenSea api key
headers = {
 "Accept": "application/json",
 "X-API-KEY": sys.argv[2]
}


os_page_size = 50
os_max_pages = 10000

date = datetime.datetime.utcnow()
since = calendar.timegm(date.utctimetuple())
since = 1628209854
os_img_count = 0

x = []
y = []

# "2021-08-29T07:05:41"

# date_time_str = '18/09/19 01:55:19'
# date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
# print(date_time_obj)


for i in range(os_max_pages):

  # Pagination offset
  offset = (i*os_page_size)

  # Load collection sales data
  url = "https://api.opensea.io/api/v1/events?collection_slug=%s&event_type=successful&only_opensea=false&offset=%s&limit=50&occurred_after=%s" % (os_slug, offset, since)
  response = requests.request("GET", url, headers=headers)
  data = json.loads(response.text)

  if not data['asset_events']:
      print("Plotted %s sales from the %s collection" % (os_img_count, os_slug))
      plt.plot(x,y)
      plt.show()
      break

  # Loop through page assets and save images in the images folder
  for item in data['asset_events']:
    if int(item['total_price']) > 0:

      x.append(datetime.datetime.strptime(item['transaction']['timestamp'], '%Y-%m-%dT%H:%M:%S'))
      y.append(int(item['total_price']) / (10.0 ** 18.0))