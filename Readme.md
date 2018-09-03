# A calculator for calculating damage in Lol

This tool is intended to allow you to simulate combat between champions in
League of Legends.  It's not working yet.

## Usage

1. Clone this repository: `git clone https://gitlab.com/Skyler827/Lol-calculator`
2. Create a python3 virtual environment: `python3 -m venv venv` (or `python` if you are on windows)
3. Activate the virtual environment:

    Command for Mac and Linux (Bash): `source venv/bin/activate`

    Command for Windows (powershell or cmd): `. .\venv\Scripts\activate.ps1`
        If you get a permission error, you will have to open a pwershell terminal as administrator and run the following command:
        `Set-ExecutionPolicy Unrestricted`
4. Update pip: `pip install --upgrade pip`
5. Install required dependencies: `pip install -r requirements.txt`
6. Run `python manage.py runserver`
7. Request: `GET http://localhost:8000/initializedb` to initialize the list of champions and download the static images
8. 

## Roadmap

Currently the tool simulates an autoattack fight between two hardcoded champions.  I will 
first make the champions configurable, then make the items and levels configurable,
then work on making sure all of the items' effects are correctly applied, then
I will start work on programming all champions spells and spell effects,
then I will implement a system for champions to determine which spells/autos/active items
to use at a given time, then i will implement the Runes, then I will refine the funcitonality 
into a well defined restful API, then I will make a front end web interface for that API,
then i will put it online somewhere.