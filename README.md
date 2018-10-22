# Create a Kerbal play/develop environment in a reproducable way

Contrary to CKAN the idea is to build everything.

# Requirements

* Kerbal(obviously) >= 1.5.0
* mono: "mono" + "msbuild-stable" on archlinux
  * If you need an IDE you might also install "monodevelop", thought a good editor and command-line should suffice.
* python >= 3.5

# Setup python venv

```
python - m venv .venv
source .venv/bin/activate
pip install - r requirements.txt
```

To reactivate the environment you always have to perform

```
source .venv/bin/activate
```

# The actual builder

Look at the help first
```
./builder.py --help
```

Also take a look at the "config.toml" file. You might want to modify that according to your needs.

The following commands are currently supported:

## install-game

Installs the game at the location definied in the "config.toml". Of course you need to purchase it first and download the zip files from the Kerbal homepage.

Please do not use pritated software. The Squad team developed a fantastic game and deserve your contribution.

## list-mods

List all the mods configured in the "config.toml" file.

## build-mod

Either use the "--all" switch to build all modules or give the name of the module you want to build.

This will retrieve the sources from the repository (usually github) and invoke "nuget" and "msbuild the way they should be invoked (or at least in a way that produce a result).

## install-mod

Either use the "--all" switch or give the name of the mod to install.

This will copy the files to the GameData folder.