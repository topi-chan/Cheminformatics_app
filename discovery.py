import os

import pandas as pd
import plotly.express as px


def visualize_compound_data(file_path: str) -> None:
    """
    Reads a compound's data from a CSV file and creates exploratory visualizations.
    Used for preliminary visualizing the data and exploratory properties of the compound for initial exploration.

    Parameters:
    file_path (str): Path to the CSV file containing the compound's activity data.
    """
    # Read the CSV file
    df: pd.DataFrame = pd.read_csv(file_path)

    # Extract the compound name from the file path
    compound_name: str = os.path.basename(file_path).split("_")[0]

    # Scatter plot: Standard Value vs. Standard Type, colored by Target Organism
    fig1 = px.scatter(
        df,
        x="standard_value",
        y="standard_type",
        color="target_organism",
        hover_data=["assay_description"],
        title=f"Standard Value vs. Standard Type by Target Organism for {compound_name}",
    )
    fig1.show()

    # Box plot: Distribution of Standard Values by Standard Type
    fig2 = px.box(
        df,
        x="standard_type",
        y="standard_value",
        title=f"Distribution of Standard Values by Standard Type for {compound_name}",
        labels={"standard_value": "Standard Value", "standard_type": "Standard Type"},
    )
    fig2.show()

    # Bar plot: Count of Activities by Target Organism
    fig3 = px.bar(
        df,
        x="target_organism",
        title=f"Count of Activities by Target Organism for {compound_name}",
    )
    fig3.show()


# Example usage:
if __name__ == "__main__":
    # Directory where your CSV files are located
    data_directory: str = "data"

    # Iterate over all files in the directory
    for filename in os.listdir(data_directory):
        if filename.endswith("_activity_data.csv"):
            filepath: str = os.path.join(data_directory, filename)
            visualize_compound_data(filepath)
