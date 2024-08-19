import xml.etree.ElementTree as ET

import requests


def fetch_pubchem_data(drug_name: str) -> dict[str, str | float | None]:
    """
    Fetches molecular data from PubChem for a given drug name.

    Parameters:
    drug_name (str): The name of the drug to fetch data for.

    Returns:
    dict: A dictionary containing molecular data from PubChem.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/property/MolecularFormula,MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,ExactMass,TPSA/JSON"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        compound_info = data["PropertyTable"]["Properties"][0]
        return {
            "Drug": drug_name,
            "Molecular Formula": compound_info.get("MolecularFormula"),
            "Molecular Weight": compound_info.get("MolecularWeight"),
            "XLogP": compound_info.get("XLogP"),
            "H-Bond Donor Count": compound_info.get("HBondDonorCount"),
            "H-Bond Acceptor Count": compound_info.get("HBondAcceptorCount"),
            "Exact Mass": compound_info.get("ExactMass"),
            "Topological Polar Surface Area (TPSA)": compound_info.get("TPSA"),
        }
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {drug_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for {drug_name}: {req_err}")
    except Exception as err:
        print(f"An error occurred for {drug_name}: {err}")

    return {}


def fetch_chembl_data(chembl_id: str) -> list[dict[str, str | None]]:
    """
    Fetches bioactivity data from ChEMBL for a given ChEMBL ID.

    Parameters:
    chembl_id (str): The ChEMBL ID of the compound to fetch data for.

    Returns:
    list: A list of dictionaries containing bioactivity data from ChEMBL.
    """
    url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id={chembl_id}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.content

        # Parse the XML content
        root = ET.fromstring(data)
        activity_data = []
        for activity in root.findall(".//activity"):
            entry = {
                "activity_id": activity.find("activity_id").text,
                "assay_description": activity.find("assay_description").text,
                "standard_type": activity.find("standard_type").text,
                "standard_value": (
                    activity.find("standard_value").text
                    if activity.find("standard_value") is not None
                    else None
                ),
                "standard_units": (
                    activity.find("standard_units").text
                    if activity.find("standard_units") is not None
                    else None
                ),
                "target_organism": (
                    activity.find("target_organism").text
                    if activity.find("target_organism") is not None
                    else None
                ),
                "target_pref_name": (
                    activity.find("target_pref_name").text
                    if activity.find("target_pref_name") is not None
                    else None
                ),
            }
            activity_data.append(entry)
        return activity_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for ChEMBL ID {chembl_id}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for ChEMBL ID {chembl_id}: {req_err}")
    except ET.ParseError as parse_err:
        print(f"Error parsing XML for ChEMBL ID {chembl_id}: {parse_err}")
    except Exception as err:
        print(f"An error occurred for ChEMBL ID {chembl_id}: {err}")

    return []
