import pandas as pd


def clean_data(
    pubchem_data: dict[str, str], chembl_data: list[dict[str, str]]
) -> tuple[dict[str, str], pd.DataFrame]:
    """
    Cleans and organizes the data gathered from PubChem and ChEMBL.

    Parameters:
    pubchem_data (dict): A dictionary containing data gathered from PubChem.
    chembl_data (list): A list of dictionaries containing activity data gathered from ChEMBL.

    Returns:
    tuple: A tuple containing two elements:
        - drug_info (dict): A dictionary containing unique drug information.
        - activity_df (pd.DataFrame): A DataFrame containing the cleaned activity data.
    """
    # Extract unique drug information
    drug_info = {
        "Drug": pubchem_data.get("Drug"),
        "Molecular Formula": pubchem_data.get("Molecular Formula"),
        "Molecular Weight": pubchem_data.get("Molecular Weight"),
        "XLogP": pubchem_data.get("XLogP"),
        "H-Bond Donor Count": pubchem_data.get("H-Bond Donor Count"),
        "H-Bond Acceptor Count": pubchem_data.get("H-Bond Acceptor Count"),
        "Exact Mass": pubchem_data.get("Exact Mass"),
        "Topological Polar Surface Area (TPSA)": pubchem_data.get(
            "Topological Polar Surface Area (TPSA)"
        ),
    }

    # Convert ChEMBL data to DataFrame
    activity_df = pd.DataFrame(chembl_data) if chembl_data else pd.DataFrame()

    return drug_info, activity_df
