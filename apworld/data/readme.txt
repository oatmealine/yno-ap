data.json:
  fetch from https://explorer.yume.wiki/data
  TODO: replace this with wrapper.yume.wiki's; that one seems better formatted and generally more complete
vms.json:
  fetch from this query url
  https://yume.wiki/api.php?action=askargs&api_version=3&format=json&conditions=-Has%20subobject::Yume%202kki:Vending%20Machine%7CVending%20Machine/Is%20implemented::true%7CVending%20Machine/Is%20accessible::true%7CVending%20Machine/Is%20secret::false&printouts=Vending%20Machine/Map%20ID%7CVending%20Machine/Event%20ID%7CVending%20Machine/Location%7CVending%20Machine/Location%20Alias&parameters=limit%3D1000
  then use the following jq query:
  [.query.results[] | .[keys[]] | {mapID: .printouts["Vending Machine/Map ID"][0], eventID: .printouts["Vending Machine/Event ID"], location: .printouts["Vending Machine/Location"][0].fulltext | split(":")[1], locationAlias: .printouts["Vending Machine/Location Alias"][0]}]
  (p.s. use the -c flag for compact output)

last updated: 0.129 patch 16 (2026-05-13)