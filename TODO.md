- [AU] Automatic - low prio

Common:
  - [ ] Figure out filler item type
  - [ ] Figure out traps
  - [ ] Vending machine locations & event IDs(?)
  - [ ] Minigame goals

APWorld:
  - [ ] Figure out how to make chance threshold more granular
  - [ ] Vending machines
    - [ ] Logic
    - [ ] Vending Machinesanity Filter
  - [ ] Masks
    - [ ] Logic
  - [ ] Events
    - [ ] Logic
  - [ ] Minigame goals
  - [x] Wallpapers
    - [ ] Logic
  - [ ] Kura Puzzles
    - [ ] Logic
  - [ ] NPCs
    - [ ] Logic
  - [x] Endings & associated logic
    - [ ] Ending #--- & Ending #...
    - [x] Win conditions
  - [x] Effect unlocks
    - [ ] Logic
  - [x] Worlds (Locationsanity)
    - [x] Logic
    - [ ] Expedition mode
    - World connection miscellanea
      - [x] Seasonal connections
      - [ ] Fix unknown chances (possibly requires better dataset)
      - [ ] Easy navigation option
      - Explicitly specify conditions
        - [ ] Fake Apartments edgecase
        - [ ] Dream Park -> Jigsaw Puzzle World - stub; cond unimplemented (Visit Jigsaw Puzzle World at least once)
        - [ ] Shadowy Caves -> Stone World - stub; cond unimplemented (Visiting Stone World at least once)
        - [ ] Balloon Park -> Legacy Nexus - stub; cond unimplemented (Night version only)
        - [ ] Firefly Clinic -> Blissful Clinic - stub; cond unimplemented (Must have visited any of the hospital rooms in Blissful Clinic)
        - [ ] Haunted Shipwreck Maze -> Quarter Flats - stub; cond unimplemented (Must have visited the Building area in Quarter Flats)
        - [ ] Sculpture Exhibition -> Head World - stub; cond unimplemented (If you visited this world before)
        - [ ] Thundercloud Cells -> Elemental Caves - stub; cond unimplemented (Visit Thunder Valley in the Elemental Caves)
        - [ ] Acid Sun Plain -> Firefly Clinic - stub; cond unimplemented (Must have visited Firefly Clinic at least once)
        - [ ] Black Cocoon Clouds -> Thundercloud Cells - stub; cond unimplemented (Must have visited Thundercloud Cells at least once)
        - [ ] Silhouette Road -> Sculpture Exhibition - stub; cond unimplemented (Must have visited the Sculpture Exhibition at least once)
        - [ ] Snail Sails -> Haunted Shipwreck Maze - stub; cond unimplemented (Must have visited the Haunted Shipwreck Maze at least once
        - [ ] Check that the following regions are truly inaccessible: ['Maiden Outlook', 'Maiden Outlook', "Unknown Child's Room", 'Deserted Center', 'Cocoa Trap Streets', 'Grayscale Mountain Ring', 'Bleeding Sorrows', 'Pastel Mall', 'Live Idol World', 'Emotional Stones', 'Snowy Fields', 'Stone Dungeon']
      - [ ] Double-triple-quadruple check the dataset is good and correct
        - This probably just requires testing it a bunch

Client:
  - [x] AP connection
    - [x] Add an AP chat tab to the right
    - [x] Implement notifications for check get/send
    - [x] Implement notifications for hint get/send
    - [ ] ~~Icons for items~~ the way this is done sucks actually
      - [ ] ~~Add icons for our own items~~

  - Effect items
    - [x] Invalidate a dream session when using a forbidden effect
    - [ ] Prevent them from being usable?
    - [ ] [AU] Award items when given them
  - Nexus key items
    - [ ] Invalidate a dream session when using a forbidden connection
    - [ ] Show a fake player to render it as inaccessible in-game
    - [ ] [AU] Wake up / abort if using it if possible?
  - [ ] Minigame items

  - UI
    - [ ] Show available effects
    - [ ] Show available minigames
    - [ ] Show possible checks in current area

  - [x] Award location on world visit
  - [ ] Award location on vending machine use
  - [ ] Award location on mask purchase
  - [ ] Award location on event trigger
  - [ ] Award location on minigame goal
  - [ ] Minigames as hint games
  - [ ] Award location on Kura Puzzle
    - [ ] Implement solve mode
  - [ ] Award location on wallpaper
    - [ ] Implement view mode
  - [ ] Award location on NPC
  - [x] Award location on ending
  - [ ] Award location on effect unlock
