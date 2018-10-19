# Create a Kerbal play/develop environment in a reproducable way

Contrary to CKAN the idea is to build everything.

# Requirements

* Kerbal(obviously) >= 1.5.0
* mono: "mono" + "monodevelop-stable" on archlinux
* actually msbuild might suffice
* python >= 3.5

# Setup python venv

```
python - m venv .venv
source .venv/bin/activate
pip install - r requirements.txt
```
