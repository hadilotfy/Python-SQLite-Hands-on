# Streamline-ETL-Reporting

A Python script designed for ETL (Extract, Transform, Load) operations with a LiteSQL database, implemented in an efficient and optimized manner.

## Description

This Python script performs the following tasks:
1. Database Creation & Initialization: Sets up a LiteSQL database.
2. Data Insertion: Inserts data into the database.
3. Data Retrieval: Reads data from the database.
4. Data Export: Exports data to CSV and JSON files.
5. Reporting: Generates insightful reports based on the data.

This project aims to streamline data management and reporting processes, making it easier to efficiently handle and analyze data.

## Requirements

in `requirements.txt` file.

## Installation

### Needed OS Packages:

   python3, python3.10-venv, pip

### Steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/hadilotfy/Streamline-ETL-Reporting.git
   ```
2. Change Directory:

   ```bash
   cd Streamline-ETL-Reporting/
   ```
3. Optional: make and activate a new virtual environment for script testing

   ```bash
   python -m venv env
   env/Scripts/activate    # or    source env/Scripts/activate
   ```
4. Install script:
   either only install the required libraries using:

   ```bash
   pip install -r requirements.txt
   ```

   or install the script to your system using:

   ```bash
   pip install .
   ```

## Usage

call the script in you shell.

```bash
   src/script.py --help
```

   or

```bash
   python src/script.py --help
```

if you installed the script using 'pip install .' , you can call using:

```bash
   hadi-etl-main.exe --help
```
