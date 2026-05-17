#!/usr/bin/env python3

# creates locations from vm data

import json
import os
from collections import defaultdict
import re

default_cost = 100
special_costs = {
  'Art Exposition I': 150,
  'Art Exposition II': 111,
  'Art Exposition III': 150,
  'Art Exposition IV': 150,
  'Art Exposition V': 150,
  'Art Exposition: Cyberpunk City': 151,
  'City of Liars': 200,
  'Coffee Cup World': 1,
  'Constellation World': 50,
  'Donut Hole World': 110,
  'Green Tile Room': 50,
  'Maple Shrine': 70,
  'Mixed Beach II': 1,
  'Pollution District': 50,
  'Pudding World': 200,
  'Scorched Wasteland': 10,
  'Shallows of Deceit': 200,
  'Subterranean Research Center': 230,
  'Urban Underworld': 200,
  'Wooden Polycube Ruins': 120,
}

# https://stackoverflow.com/a/47713392
ROMAN = [
  (1000, "M"),
  ( 900, "CM"),
  ( 500, "D"),
  ( 400, "CD"),
  ( 100, "C"),
  (  90, "XC"),
  (  50, "L"),
  (  40, "XL"),
  (  10, "X"),
  (   9, "IX"),
  (   5, "V"),
  (   4, "IV"),
  (   1, "I"),
]

def to_roman(number):
  result = ""
  for (arabic, roman) in ROMAN:
    (factor, number) = divmod(number, arabic)
    result += roman * factor
  return result

output_dir = os.path.join(os.path.dirname(__file__), '..', 'client', 'locations', 'vms')

for file in os.listdir(output_dir):
  if file.endswith('.json'):
    os.remove(os.path.join(output_dir, file))

with open(os.path.join(os.path.dirname(__file__), '..', 'apworld', 'data', 'vms.json'), 'r') as file:
  vms = json.load(file)

  vm_counts = defaultdict(int)

  for vm in vms:
    location_name = vm["locationAlias"]
    vm_counts[location_name] += 1

  vm_index = defaultdict(int)

  for vm in vms:
    location_name = vm["locationAlias"]

    count = vm_counts[location_name]
    index = vm_index[location_name]

    name = f"{location_name}"
    if count > 1:
      name += f" {to_roman(index + 1)}"
      vm_index[location_name] += 1

    filename = re.sub(r"[^a-z\d\w-]", '_', name.lower()) + '.json'

    cost = default_cost
    if vm["location"] in special_costs:
      cost = special_costs[vm["location"]]
    if vm["locationAlias"] in special_costs:
      cost = special_costs[vm["locationAlias"]]
    if name in special_costs:
      cost = special_costs[name]

    with open(os.path.join(output_dir, filename), 'w') as out:
      json.dump({
        'name': f'Vending Machine - {name}',
        'condition': {
          'map': int(vm['mapID']),

          'trigger': 'eventAction',
          'values': [str(int(evid)) for evid in vm['eventID']],

          'varId': 10000,
          'varValue': cost,
          'varOp': '>=',
        }
      }, out, separators=(',', ':'), ensure_ascii=False)