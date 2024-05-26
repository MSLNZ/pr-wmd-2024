This code was used for the light-bulb demonstration for World Metrology Day 2024.

Three 34401A DMMs are used to measure either AC voltage or AC current for an LED bulb
and a Halogen bulb and a web server is used to display the values in real time.

Prerequisites
-------------
[Python](https://www.python.org/downloads/) (with the `py`-Launcher option enabled) and [Git](https://git-scm.com/downloads).

Set up
------
Run the following commands in a terminal to set up the Python environment

```console
> git clone https://github.com/MSLNZ/pr-wmd-2024.git
> cd pr-wmd-2024
> py -m venv .venv
> .venv\Scripts\activate
> pip install -r requirements.txt
```

Run
---
1. Update the `records` dictionary in `equipment.py` for the three DMMs that are used, 
in particular, edit the `COM#` address value.

2. Run the following command to start acquiring data and to start the web server

```console
> run.bat
```

Source Files
------------
* `acquire.py` Runs in a loop to send voltage and current values to the web server.
* `equipment.py` Provides communication to a 34401A DMM to either measure voltage or current.
* `webapp.py` Runs a web server to display the voltage and current values in real time.
