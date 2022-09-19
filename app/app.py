# this gets property information from a realtor website
# teases it apart,
# and saves it to a file
# using selenium in colab - https://gist.github.com/korakot/5c8e21a5af63966d80a676af0ce15067

# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

import lxml
from bs4 import BeautifulSoup
import time
import json
import random
import flatten_dict
from flatten_dict import flatten
import pandas as pd
import datetime as dt

# url for the web page
# url = "https://www.realtor.com/realestateandhomes-search/Jefferson-County_KY/beds-4/show-recently-sold"
url = "https://www.realtor.com/realestateandhomes-search/Middletown_KY/beds-4/type-single-family-home/show-recently-sold?view=map&pos=38.38153,-85.708911,38.147009,-85.09093,11&qdm=true&points=bn%60jOkyqhFwXdnBqnB%7CtB_dClbAiqElg%40g%7DWbIw%7DCyOoyCu%7B%40qpA_uB%3Fmg%40xv%40u%7B%40~lEadBxbHyj%40~fS_d%40vaBad%40fjBvEjhCvj%40t_C%7CtB"
browser = webdriver.Chrome(options=options)
browser.get(url)
# time.sleep(5)

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

# the property data is in the page within this tag: <script id="__NEXT_DATA__" type="application/json">
prop_data = soup.find(id="__NEXT_DATA__")

# the first element of the bs object is the string of the property data json
prop_dict = json.loads(prop_data.contents[0])

# let's investigate the nested json structure
# show the top level keys of the nested json
# prop_dict.keys()

# create the flattened version of the nest
# flat_prop = flatten(prop_dict, reducer='underscore')

# flat_prop.keys()

"""
for k,v in flat_prop.items():
  print(f"key: {k}")
  if isinstance(v, list):
    print(f"v: {len(v)} values ---------------- **************** ---------------")
  else:
    print(f"v: {v}")
"""

# the actual properties data is nested here
r = prop_dict["props"]["pageProps"]["searchResults"]["home_search"]["results"]

# print(f"there are {len(r)} properties.")

# a random property for inspection
# random_prop = r[random.randint(0,len(r)-1)]

# here are the keys for the specific property data
# assumption is that these keys exist for all properties, but that should be verified
# random_prop.keys()

flat_result = flatten(r[4], reducer='underscore')
# flat_result

# we only care about data from keys that start with these strings
keys_starts_with_list = ["property_id", "description_", "location_", "tax_record"]

# what keys from r[4] start with a string in the starts_with list
good_key = []
for k in flat_result.keys():
  for s in keys_starts_with_list:
    if k.startswith(s):
      good_key.append(k)
      break
  
# good_key

# make a list of the flattened results
p_list = []
for p in r:
  p_list.append(flatten(p, reducer='underscore'))
# make a dataframe
p_df = pd.DataFrame(p_list)
# then drop the columns that aren't 'good_key' columns
p_df.drop(columns=p_df.columns.difference(good_key), inplace=True)

# output the result to a local time-stamped csv file
name = "out/out" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
p_df.to_csv(name)

print(f"saving output to: {name}")