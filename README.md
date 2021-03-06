# VidaBlue
A map maker for ascii roguelikes.

## File Format(s)
Maps are currently stored in the following way:
  * **_map* - This is a text file representing a grid of size width and height, with each character matching the character at that position in the map you created.
  * **_solidity.txt* - This is a grid of either 0's or 1's denoting whether or not you have marked that tile as solid in the map editor.
  * **_interact.txt* - This is a grid of either 0's or 1's denoting whether or not you have marked that tile as interactable in the map editor.
  * **_properties.txt* - This is a file where each line contains the properties of a single tile you have given properties to in the editor. The format of this line looks like:
    ``` xpos,ypos,name,description ```

## How To Use
  * Ctrl - Place char, start/end line, denote solid/interactable, edit properties of current tile.
  * Space - Select menu items when paused.
  * Left and Right Bracket - cycle through drawing/selecting tools.
  * Arrow Keys - Move cursor on screen
  * Tab - Change editing mode (char, solidity, interactable, or properties).
  * Escape - Bring up pause menu.
  * Any normal keyboard char - selects char to be used.
  * Shift - Switches current char with alternate char.

## Saving A Map
  When saving a map, the VidaBlue will produce 4 seperate files in the "out" folder with the given name.
  
  (See first section for breakdown of these files)

## Loading A Map
  When loading a map, select **all** files that start with the name of the map you want to edit, so VidaBlue can properly load all aspects of it. Do this by opening **all** the files when prompted to select a file to load, VidaBlue will figure out which file is which.

## Todo
  * Way to input none keyboard friendly ascii chars
  * User fonts (currently the only you can use is square.tff which is 12px)
  * Copy and Paste tool
  * Prefab support

## Dependencies:
  ```pip install bresenham easygui bearlibterminal```