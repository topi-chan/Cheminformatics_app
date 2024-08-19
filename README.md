# Cheminformatics Data Processing and Visualization App

## Overview

This application processes cheminformatics data, cleans it, and visualizes key metrics through an interactive Dash-based web interface. The tool can either gather and clean data, run a Dash app, or perform both actions depending on the command-line arguments provided. With current setup, the app shows ED50/TD50 information for anticonvulsant drugs.

## Features

- **Data Gathering**: Fetches data from ChEMBL and PubChem APIs based on provided compound names and IDs.
- **Data Cleaning**: Cleans and formats the gathered data, preparing it for analysis.
- **Data Visualization**: Generates interactive plots (ED50 vs. TD50) for each compound and visualizes organism test frequencies.
- **Interactive Dash App**: Presents the data through a user-friendly web interface with the ability to navigate between different views.
- **Current setup**: presents ED50 and TD50 for chosen anticonvulsant drugs and presents number of organisms used in research.

## Details - how to use

- **For basic run just install requirements in venv (pip install -r requirements.txt) and type python main.py** in main project directory. App should be available at 127.0.0.1:8050 address.
- Basic compounds.csv file is provided for anticonvulsant drugs. To add drugs, enter name of active compound and check ChEMBL ID on https://www.ebi.ac.uk/chembl/compound_report_card/. Add it to compounds.csv file following formatting provided there (active_compound,ID. 
- You can add more compounds files and pass them when running the app, example: python main.py --compound-file compounds_2.csv. The file has to be in csv format and follow compounds.csv formatting.
- You can type --run-mode as "gather", "run" or "gather-and-run".
- For help type python main.py --help or python main.py -h.
- You can run python discovery.py for fast pre-analysis of data. It uses express plotly version.
- Drug details, after fetching from databases and formatting, are saved in data and drug_info directories. If directories are not present, they are automatically created. After you re-run the app, currently existing files are replaced (if you fetch data for same drugs).
- For some drugs there are no research data, so they are not presented in the app, but basic details will still be saved in drug_info directory (e.g. for topiramate).
- Application was developed on Python 3.11. It will not work on Python 3.8 and below, due to different typehints syntax. It is recommended to use Python 3.11+.

## Improvements

- Application is modular, so functions can be used for different types of visualizations and possibly in another apps too.
- More views can be added in dash_app module, or new file, such as views.py, can be created.
- So far code is not repetitive enough to introduce OOP approach, but in future it might be reasonable.
- More data sources may be used for more thoughtful/deeper analysis. For example: DrugBank, PDB, ZINC Database.
- To develop app it's highly recommended to use black (black . in main directory) and then isort (isort .). For development install dev requirements (pip install -r requirements_dev.txt).

## Conclusions

- From gathered data it seems that newer anticonvulsant drug - lamotrigine - is safest, when it comes to ED50/TD50 comparison.
- Another newer drug, pregabalin, do not have enough studies in vivo when it comes to anticonvulsant capabilities, so it was excluded from analysis (app only show number of tests on a subpage for the drug).
- Data currently gathered in the app is rather spare, so it is essential to analyse wider data to draw any clinically relevant conclusions.
