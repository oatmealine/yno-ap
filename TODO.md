- [AU] Automatic - low prio

Common:
  - [ ] Figure out filler item type
  - [ ] Figure out traps
  - [x] Vending machine locations & event IDs(?)
  - [ ] Minigame goals

APWorld:
  - [ ] Figure out how to make chance threshold more granular
  - [x] Vending machines
    - [x] Logic (kind of? needs testing)
    - [x] Vending Machinesanity Filter
  - [ ] Masks
    - [ ] Logic
  - [x] Events
    - [x] Logic
  - [ ] Minigame goals
  - [x] Wallpapers
    - [ ] Logic
  - [ ] Kura Puzzles
    - [ ] Logic
  - [x] NPCs
    - [x] Logic
  - [x] Endings & associated logic
    - [ ] Ending #--- & Ending #...
    - [x] Win conditions
  - [x] Effect unlocks
    - [x] Logic
  - [x] Author gating
    - [ ] Contributing author gating
  - [x] Worlds (Locationsanity)
    - [x] Logic
    - [ ] Expedition mode
    - World connection miscellanea
      - [x] Seasonal connections
      - [ ] Fix unknown chances (possibly requires better dataset)
      - [ ] Easy navigation option
      - Explicitly specify conditions
        - [x] Specify all explicit conditions
        - [x] Fake Apartments edgecase
        - [ ] Check that the following regions are truly inaccessible: ['Maiden Outlook', "Unknown Child's Room", 'Deserted Center', 'Cocoa Trap Streets', 'Grayscale Mountain Ring', 'Gallery of Me', 'Ironashi Coast', 'Live Idol World', 'Emotional Stones']
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
    - [x] Invalidate a dream session when using a forbidden connection
    - [ ] Show a fake player to render it as inaccessible in-game
    - [ ] [AU] Wake up / abort if using it if possible?
  - [ ] Minigame items
  - [ ] Text events invalidation
  - [ ] Author gating

  - UI
    - [ ] Show available effects
    - [ ] Show available minigames
    - [ ] Show possible checks in current area

  - [x] Award location on world visit
  - [x] Award location on vending machine use
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
  - [x] Award location on effect unlock
  - [x] Goal whenever prerequisites are met
