# VaporOS Flatpak Manager
VaporOS Flatpak Manager allows you to easily install software on SteamOS through Flatpak. It doesn't require a mouse and keyboard, since it can also be controller with a gamepad. It has been created using Python and the pygame engine.

### Screenshot

![](https://github.com/sharkwouter/vaporos-flatpak-manager/raw/master/screenshot.png)

### Requirements

VaporOS Flatpak Manager requires the following python packages to be installed:

- pygame
- requests
- appdirs

And the following additional software:

- Flatpak
- The Liberation Sans Narrow font

### TODO

Before VaporOS Flatpak Manager can be considered done, the following changes will need to be made:

- ~~Make compatible with python 3 by using the ``threading`` module~~
- ~~Show installation progress~~
- ~~Prevent inputs from being registered multiple times~~

These features would be nice to have:

- Add button prompts to the bottom bar
- Create shortcuts in Steam
- ~~Fix main menu looks at 720p~~
- ~~add more keyboard binds~~
- Center content on application buttons better on high resolution displays
- Add more screenshots
- Controller specific button prompts
- Allow for running updates (this could initially be solved outside of the application)
- ~~Allow software installation to happen in the background~~
- Package for Arch
- Delete runtimes which are no longer needed when uninstalling software

### Licensing on Assets

The icon data/vaporos-flatpak-manager.png was found on (Wikimedia)(https://commons.wikimedia.org/wiki/File:Storage_icon.svg), created by PanierAvide and licensed under the [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/deed.en) license.
