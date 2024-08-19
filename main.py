import argparse
import os

import pandas as pd

from dash_app import (create_dash_app, create_visualizations,
                      load_compound_list, load_data)
from data_cleaning import clean_data
from data_gathering import fetch_chembl_data, fetch_pubchem_data


def gather_and_clean_data(compound_file: str) -> None:
    """
    Gathers and cleans data for each compound in the input file.

    Parameters:
    compound_file (str): The path to the CSV file containing compound names and ChEMBL IDs.
    """
    # Read the CSV file containing compound names and ChEMBL IDs
    compounds: pd.DataFrame = pd.read_csv(compound_file)

    # Create a directory for the drug information if it doesn't exist
    os.makedirs("drug_info", exist_ok=True)

    # Process each compound
    for index, row in compounds.iterrows():
        compound_name: str = row["compound_name"]
        chembl_id: str = row["chembl_id"]

        print(f"Processing {compound_name} (ChEMBL ID: {chembl_id})...")

        # Step 1: Gather data
        pubchem_data: dict = fetch_pubchem_data(compound_name)
        chembl_data: list = fetch_chembl_data(chembl_id)

        # Step 2: Clean data
        drug_info, activity_df = clean_data(pubchem_data, chembl_data)

        # Save drug information
        drug_info_df: pd.DataFrame = pd.DataFrame([drug_info])
        drug_info_file: str = f"drug_info/{compound_name}_info.csv"
        drug_info_df.to_csv(drug_info_file, index=False)
        print(f"Drug information for {compound_name} saved to {drug_info_file}.")

        # Step 3: Save the cleaned activity data

        # Ensure the directory exists
        os.makedirs("data", exist_ok=True)

        # Save the DataFrame to a CSV file
        if not activity_df.empty:
            activity_df.to_csv(f"data/{compound_name}_activity_data.csv", index=False)
            print(
                f"Activity data for {compound_name} saved to data/{compound_name}_activity_data.csv\n"
            )
        else:
            print(f"No activity data for {compound_name}. Skipping save.")


def main(compound_file: str, run_mode: str) -> None:
    """
    Main function that either gathers and cleans data or gathers, cleans, and starts the Dash app.

    Parameters:
    compound_file (str): The path to the CSV file containing compound names and ChEMBL IDs.
    run_mode (str): The mode of operation: 'gather', 'run', or 'gather_and_run'.
    """
    if run_mode in ["gather", "gather-and-run"]:
        # Gather and clean data
        gather_and_clean_data(compound_file)

    if run_mode in ["run", "gather-and-run"]:
        # Load and start the Dash app
        compounds_df, compounds = load_compound_list(compound_file)
        data, properties = load_data("data", compounds)
        if data:
            figures = create_visualizations(data)
            if figures:
                app = create_dash_app(figures, properties, data)
                app.run_server(debug=False)


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Process compound data and optionally start a Dash app."
    )

    # Set default file location to 'compounds.csv'
    parser.add_argument(
        "--compound-file",
        type=str,
        default="compounds.csv",
        help="Path to the CSV file with compound names and ChEMBL IDs. Defaults to 'compounds.csv'.",
    )

    parser.add_argument(
        "--run-mode",
        type=str,
        choices=["gather", "run", "gather-and-run"],
        default="gather-and-run",
        help="""Choose the mode: 'gather' to only gather data, 'run' to only run the Dash app, 
                        or 'gather-and-run' to gather data and then run the app. Defaults to 'gather-and-run'.""",
    )

    args = parser.parse_args()

    # Run the main function with the provided arguments
    main(args.compound_file, args.run_mode)
