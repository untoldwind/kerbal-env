# Create a Kerbal play/develop environment in a reproducable way

Contrary to CKAN the idea is to build everything.

# Requirements

* Kerbal(obviously) >= 1.8.0
* On Linux:
  * mono: "mono" + "msbuild-stable" on archlinux
    * If you need an IDE you might also install "monodevelop", thought a good editor and command-line should suffice.
* On Windows:
  * Command-line version of the C# compiler (csc.exe), either by installing the Microsoft build tools (VisualStudio) or
     `nuget install Microsoft.Net.Compilers`

* python >= 3.5

# Setup python venv

On Windows (in regular Commanline cmd.exe)

```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

On Linux:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To reactivate the environment you always have to perform

```
source .venv/bin/activate
```
(There are some other variants depending on the shell you are using)

# The actual builder

Look at the help first
```
python builder.py --help
```

On Linux you may also just use

```
./builder.py --help
```


Also take a look at the "config.toml" file. You might want to modify that according to your needs.

The following commands are currently supported:

## install-game

Installs the game at the location definied in the "config.toml". Of course you need to purchase it first and download the zip files from the Kerbal homepage.

Please do not use pritated software. The Squad team developed a fantastic game and deserve your contribution.

Note: This only works with the portable .zip version of the game. When using the windows-installer this step is entirely unnecessary.

## list-mods

List all the mods configured in the "config.toml" file.

## build-mod

Either use the "--all" switch to build all modules or give the name of the module you want to build.

This will retrieve the sources from the repository (usually github) and invoke "nuget" and "msbuild the way they should be invoked (or at least in a way that produce a result).

After some messup I decided to ignore msbuild and invoke csc directly. This might be more cumbersome, but allows much better control over what is linked with what.

## install-mod

Either use the "--all" switch or give the name of the mod to install.

This will copy the files to the GameData folder.

# Reasons why to prefer this over CKAN

As a games/Mod-User ... probably none at all.

As a (potential) mod-developer or someone generally interested in software this tool might safe the day.

When developing a mod I always found the most annoying task to setup the development environment. Moreover, when tweaking mods written by someone else one always has to figure out how this specific developer is doing things. Yes, "msbuild" is more or less standard, but there are so many ways using (or misusing) it and of course there a compatibility issues between linux and windows. Finding a mod where "msbuild" works out of the box ony any operating system are actually pretty rare (kudos to all develops actually investing time in doing so).

"kerbal-env" does not try to solve this problem. I.e. is is not meant to be a replacement for "msbuild" or any other build tool for that matter. Instead it is a meant to be a form of documentation how this or that mod has to be build. When writing a receipt one still has to figure out how things are working together or where meant to be. The whole point is: You only have to do it once.

# Notes

The setup was tested on Linux with the game purchased and downloaded from the kerbalspaceprogram.com website. There is no reason why it should not work with the Steam version as well (except the "install-game" command of course), you just have to change the "game_dir" in the config.toml (to .local/share/Steam/steamapps/common/Kerbal most likely)

On windows things might be different though. Python exists on windows and most of the code should be platform independent, but nothing was tested in that direction so far. I have not done any kind of development on windows for decades.

## EVE

At the moment EVE is deployed as is, since it is actually pretty complicated to bundle shaders correctly.

## Scatterer

Like EVE it is deployed as is for the same reasons, but disabled for now since it seems to create wierd effects (at least on my machine).

## KAS

KAS is deployed with the LEGACY code, but without the corresponding parts. This is just for compatibility with other mods (namely MKS).
If you have a save game containing legacy KAS part you either have to patch the `KAS.py` receipt or your save game file.

