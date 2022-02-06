import datetime
import matplotlib.pyplot as plt
import numpy as np
import requests
import sys
import urllib.request, json

# OpenSea collection slug
os_slug = sys.argv[1]

# OpenSea api key
headers = {
 "Accept": "application/json",
 "X-API-KEY": sys.argv[3]
}

#  Since timestamp
since = int(datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%S').timestamp())

os_page_size = 50
os_max_pages = 10000

sales_count = 0

x = []
y = []

cum_price = 0.0

for i in range(os_max_pages):

  # Pagination offset
  offset = (i*os_page_size)

  # Load collection sales data
  url = "https://api.opensea.io/api/v1/events?collection_slug=%s&event_type=successful&only_opensea=false&offset=%s&limit=50&occurred_after=%s" % (os_slug, offset, since)
  response = requests.request("GET", url, headers=headers)
  data = json.loads(response.text)


  if not data['asset_events']:
      print("Plotted %s sales from the %s collection" % (sales_count, os_slug))
      plt.plot(x,y)
      plt.show()
      break

  # Loop through asset events and assign plot variables
  for item in data['asset_events']:
    if int(item['total_price']) > 0:

      x.append(datetime.datetime.strptime(item['transaction']['timestamp'], '%Y-%m-%dT%H:%M:%S'))
      y.append(int(item['total_price']) / (10.0 ** 18.0))
      sales_count += 1