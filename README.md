# Python-SQLite-Hands-on

This is a demo for ETL python script.

## Description

This is a python script to create and initialize a liteSQL db, add data to the db, read the data from the DB, dump to CSV and JSON files, then read those files and generate a report that provides some insights in the data.

## Requirements

in `requirements.txt` file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hadilotfy/Python-SQLite-Hands-on.git
   ```
2. Enter the repo directory:

   ```bash
   cd Python-SQLite-Hands-on
   ```
3. Optional: make and activate a new virtual environment for script testing

   ```bash
   python -m venv env
   env/Scripts/activate
   ```
4. Install script:
   either only install the requirement using:

   ```bash
   pip install -r requirements.txt
   ```

   or install the script to your system using:

   ```bash
   pip install .
   ```

## Usage

call the script in you shell.

    python src/script.py --help

    or

    src/script.py -h

if you installed the script using 'pip install .' , you can call using:

    hadi-etl-main.exe -h
