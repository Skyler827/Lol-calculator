# A calculator for calculating damage in Lol

This tool is intended to allow you to simulate combat between champions in
League of Legends.  It's not working yet.

## Usage

1. Clone this repository: `git clone git@github.com:Skyler827/Lol-calculator.git`
2. Create a python3 virtual environment: `python3 -m venv venv` (or `python` if you are on windows)
3. Activate the virtual environment:

    Command for Mac and Linux (Bash): `source venv/bin/activate`

    Command for Windows (powershell or cmd): `. .\venv\Scripts\activate.ps1`
    
    If you get a permission error, open a pwershell terminal as administrator and run the following command:
        `Set-ExecutionPolicy Unrestricted`
4. Update pip: `pip install --upgrade pip`
5. Install required dependencies: `pip install -r requirements.txt`
6. Run `python manage.py runserver`
7. Request: `GET http://localhost:8000/initializedb` to initialize the list of champions and download the static images
8. View the web app at http://localhost:8000 in your browser.

## Roadmap

1. Simulates an autoattack fight between two champions: **_Done_**
2. Basic Web interface: **_Done_**
3. Items and Champs are editable: **_Done_**
4. Item basic stats apply correcly: _In progress_
5. Basic Stats show in user interface: _Next_
5. Health and Mana regeneration: _After that_
5. Two champions' spells: _Later_
6. Procedure for handling spell choice and timing: _Later_
7. Combat Summoner Spells are incorporated: _Later_
8. \~Twenty Champions' spells: _Later_
9. Some Item Actives and effects: _later_
10. Runes Reforged: _Later_
11. All other champions' spells/other items: _Later_
