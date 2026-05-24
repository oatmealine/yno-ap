#!/usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.requests

# downloads, merges and reformats results for yume.wiki API queries

import requests
from urllib.parse import urlencode, quote
import json
import re

API_BASE = "https://yume.wiki/api.php"
FETCH_LIMIT = 500
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
CF_CLEARANCE = "L5C89HJrqGhsAzRLugR3SfNkv3SpHK3sHCMdG6oJoAA-1779564936-1.2.1.1-UiItgRberic27eNFZKD_dGng.8WeTpowPNiBEIHmGWOVM29zLSqJUTieeZ1fpNmGu9NFU5bxP_VYLGruzJuV8sRGEIWMafv5cLmAda8HGbYLtfOs9yqrf2zkIdXNhZP_r_8ZQEy13_Yv_rei_iFr2MuuHTvybIwfg2RlZpHTeR9Dsj5mBCPFvFW.TYSlwBBp4YKH3uXzenH0.V4J3xmGmSWuj4XQ2grHjswqeqeQvMlrwpZ3Yj25XCCrY5lEui6gr4Hw984QC8.At44rV57SCMBQhY8VTtNG7NlZII5llS2NAD.W_2T0OXUQxfh8V9Avuh6aTYIchBdmgyIJWZkm7LTGoTWwIutz0WgW8tlwKw815_wF.mm7cc7wKucdnf66tLfyS4ie.QzTs9xNqbEnuJsPIvVBh6O7e1nipBAbUsc"

def query(conditions: list[str], printouts: list[str]) -> dict[str, any]:
  i = 0
  offset = 0
  results = {}
  while True:
    parameters = {
      "limit": FETCH_LIMIT,
      "offset": offset,
    }

    search_params = urlencode({
      "action": "askargs",
      "api_version": "2",
      "format": "json",
      "conditions": str.join("|", conditions),
      "printouts": str.join("|", printouts),
      "parameters": str.join("|", (f"{key}={value}" for key, value in parameters.items())),
    }, doseq=True, quote_via=quote, safe=":/")

    url = API_BASE + "?" + search_params

    print(f"  req {i + 1}: offset={offset}")
    r = requests.get(url, headers={
      "user-agent": USER_AGENT,
      "cookie": f"cf_clearance={CF_CLEARANCE}",
    })
    print(f"  {r.status_code} {r.reason} {round(len(r.content) / 1024 * 10)/10}KB")

    if not r.ok:
      print(r.text)
      raise Exception(f"""
  Server returned non-200 response; likely a CF block page. See above for more details.
  Try going on the following page and resolving the captcha:
  {url}
  Afterwards, copy the cf_clearance cookie from your browser, and paste it (alongside with your user agent) at the top of this script.""")

    data = r.json()

    if "error" in data:
      raise Exception(f"Got error from server:\n{"\n".join(data["error"]["query"])}")

    if "query" not in data:
      print(data)
      raise Exception("query not found in data. This indicates a broken API query")

    results |= data["query"]["results"]

    if "query-continue-offset" in data:
      offset = data["query-continue-offset"]
    else:
      break

    i = i + 1

  return results

def strip_namespace(s: str):
  return s.split(":")[1]

def transform_vm(vm: dict[str, any]):
  printouts = vm["printouts"]

  return {
    "mapID": printouts["Vending Machine/Map ID"][0],
    "eventID": printouts["Vending Machine/Event ID"],
    "location": strip_namespace(printouts["Vending Machine/Location"][0]["fulltext"]),
    "locationAlias": printouts["Vending Machine/Location Alias"][0]
  }

def fetch_vms():
  vms_data = query(
    conditions=[
      "-Has subobject::Yume 2kki:Vending Machine",
      "Vending Machine/Is implemented::true",
      "Vending Machine/Is accessible::true",
      "Vending Machine/Is secret::false",
    ],
    printouts=[
      "Vending Machine/Map ID",
      "Vending Machine/Event ID",
      "Vending Machine/Location",
      "Vending Machine/Location Alias",
    ]
  )

  return list(map(transform_vm, vms_data.values()))

def transform_world(data: tuple[str, dict[str, any]]):
  name, world = data
  printouts = world["printouts"]

  return {
    "name": strip_namespace(name),
    "primaryAuthors": printouts["Has primary author"],
    "contributingAuthors": printouts["Has contributing author"],
  }

def fetch_worlds():
  world_data = query(
    conditions=[
      "Category:Yume 2kki Locations",
      "Accessible::true"
    ],
    printouts=[
      "Has primary author",
      "Has contributing author"
    ]
  )

  return list(map(transform_world, world_data.items()))

def transform_connection(connection: dict[str, any]):
  printouts = connection["printouts"]

  conn_type = 0
  conn_params = {}
  attributes = printouts["Connection/Attribute"]
  for attribute in attributes:
    # https://github.com/Flashfyre/Yume-2kki-Explorer/blob/dce472e20ceacc66acd41417a9f0a345f7acd513/app.js#L1147
    if attribute == "No Return":
      conn_type |= 1
    if attribute == "No Entry":
      conn_type |= 2
    if attribute == "Unlockable":
      conn_type |= 4
    if attribute == "Locked":
      conn_type |= 8
    if attribute == "Dead End":
      conn_type |= 16
    if attribute == "Return":
      conn_type |= 32
    if attribute == "Needs Effect":
      conn_type |= 64
      effects = str.join(",", printouts["Connection/Effects needed"])
      effects = effects.replace('Teru Teru Bozu', 'Teru Teru Bōzu')
      effects = effects.replace('Gakuran', 'School Boy')
      effects = effects.replace('&comma;', ',')
      effects = effects.replace(';', ',')
      effects = effects.replace(' or ', ',')
      conn_params[64] = [effect.strip() for effect in effects.split(',')]
    if attribute == "Chance":
      conn_type |= 128
      conn_params[128] = printouts["Connection/Chance percentage"][0]
    if attribute == "Conditional":
      conn_type |= 256
      cond_text = printouts["Connection/Unlock conditions"][0]
      # backported text fixes from 2kki explorer
      cond_text = re.sub(r"^Require(s|d) (to )?", "", cond_text)
      cond_text = re.sub(r"\.$", "", cond_text)
      cond_text = cond_text[0].upper() + cond_text[1:]
      conn_params[256] = cond_text
    if attribute == "Shortcut":
      conn_type |= 512
    if attribute == "Exit Point":
      conn_type |= 1024
    if attribute == "Seasonal":
      conn_type |= 2048
      conn_params[2048] = printouts["Connection/Season available"]

  return {
    "from": strip_namespace(printouts["Connection/Origin"][0]["fulltext"]),
    "to": strip_namespace(printouts["Connection/Location"][0]["fulltext"]),
    "type": conn_type,
    "params": conn_params,
  }

def fetch_connections():
  connection_data = query(
    conditions=[
      "Yume 2kki:+",
      "Is subobject type::connection",
      "Connection/Is removed::false"
    ],
    printouts=[
      "Connection/Origin",
      "Connection/Location",
      "Connection/Attribute",
      "Connection/Unlock conditions",
      "Connection/Effects needed",
      "Connection/Season available",
      "Connection/Chance percentage",
      "Connection/Chance description",
    ]
  )

  return list(map(transform_connection, connection_data.values()))

def transform_collectible(wallpaper: dict[str, any]):
  printouts = wallpaper["printouts"]
  title = printouts["Collectible/Title"]
  return {
    "id": printouts["Collectible/ID"][0],
    "title": title[0] if len(title) > 0 else None,
    "cond": printouts["Collectible/Condition"][0],
  }

def fetch_wallpapers():
  wallpapers_data = query(
    conditions=[
      "Collectible/Type::Wallpaper",
      "Collectible/Game::Yume 2kki",
      "Collectible/Is removed::false"
    ],
    printouts=[
      "Collectible/ID",
      "Collectible/Title",
      "Collectible/Condition"
    ]
  )

  return list(map(transform_collectible, wallpapers_data.values()))

def fetch_kura_puzzles():
  kura_puzzle_data = query(
    conditions=[
      "Collectible/Type::Kura Puzzle",
      "Collectible/Game::Yume 2kki",
      "Collectible/Is removed::false"
    ],
    printouts=[
      "Collectible/ID",
      "Collectible/Title",
      "Collectible/Condition"
    ]
  )

  return list(map(transform_collectible, kura_puzzle_data.values()))

def write_data(func, filename):
  print(filename)
  with open(filename, "w") as out:
    json.dump(func(), out, separators=(',', ':'), ensure_ascii=False)
  print("  merged; done")

if __name__ == "__main__":
  write_data(fetch_worlds, "worlds.json")
  write_data(fetch_connections, "connections.json")
  write_data(fetch_vms, "vms.json")
  write_data(fetch_wallpapers, "wallpapers.json")
  write_data(fetch_kura_puzzles, "kura_puzzles.json")