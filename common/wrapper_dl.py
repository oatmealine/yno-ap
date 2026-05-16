#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.requests

# downloads and merges results for a wrapper.yume.wiki query into a single json
# usage: wrapper_dl.py https://wrapper.yume.wiki/locations?game=2kki > locations.json

import sys
import requests
import urllib.parse
import json

url_str = sys.argv[1]
url = urllib.parse.urlsplit(url_str, allow_fragments=False)
query = urllib.parse.parse_qs(url.query)
if "continueKey" in query: del query["continueKey"]

merged = {"data": None}

# loosely based on https://stackoverflow.com/a/7205672
def merge(dict1, dict2):
  dict_new = {}
  for k in set(dict1.keys()).union(dict2.keys()):
    if k not in dict2 or dict2[k] is None:
      dict_new[k] = dict1[k]
    elif k not in dict1 or dict1[k] is None:
      dict_new[k] = dict2[k]
    elif isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
      dict_new[k] = merge(dict1[k], dict2[k])
    elif isinstance(dict2[k], list) and isinstance(dict2[k], list):
      dict_new[k] = dict1[k] + dict2[k]
    else:
      dict_new[k] = dict2[k]
  return dict_new

continue_key = None
i = 0
while True:
  if continue_key is not None:
    query["continueKey"] = continue_key
    url = url._replace(query=urllib.parse.urlencode(query, doseq=True))

  print(f"req {i + 1}: {url.geturl()}", file=sys.stderr)
  r = requests.get(url.geturl())
  print(f"{r.status_code} {r.reason} {round(len(r.content) / 1024 * 10)/10}KB", file=sys.stderr)

  data = r.json()

  merged = merge(merged, {"data": data})

  if isinstance(data, dict) and "continueKey" in data:
    continue_key = data["continueKey"]
  else:
    break

  i = i + 1

merged_data = merged["data"]
if isinstance(merged_data, dict) and "continueKey" in merged_data: del merged_data["continueKey"]

json.dump(merged_data, sys.stdout, separators=(',', ':'), ensure_ascii=False)