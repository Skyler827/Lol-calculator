#A calculator for calculating damage in Lol

This tool is intended to allow you to simulate combat between champions in
League of Legends.  It's not working yet.

## Usage

\1. Clone this repository

`git clone https://gitlab.com/Skyler827/Lol-calculator`
\2. Create a python3 virtual environment

`python3 -m venv venv`
\3. Activate the virtual environment

Command for Mac and Linux:
`source venv/bin/activate`
Command for Windows: (coming soon!)
\4. Install required dependencies:

`pip install -r requirements.txt`
\5. Run `initializedb.py`

\6. Run `python timer.py`

## Roadmap

Currently the tool simulates an autoattack fight between two hardcoded champions.  I will 
first make the champions configurable, then make the items and levels configurable,
then work on making sure all of the items' effects are correctly applied, then
I will start work on programming all champions spells and spell effects,
then I will implement a system for champions to determine which spells/autos/active items
to use at a given time, then i will implement the Runes, then I will refine the funcitonality 
into a well defined restful API, then I will make a front end web interface for that API,
then i will put it online somewhere.