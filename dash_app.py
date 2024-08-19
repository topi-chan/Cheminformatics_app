import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output


# Step 1: Load the compound list
def load_compound_list(compound_file: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Load the list of compounds from a CSV file.

    Args:
        compound_file (str): The path to the CSV file containing the compound list.

    Returns:
        tuple[pd.DataFrame, list[str]]: A tuple containing the DataFrame of compounds and a list of compound names.
    """
    print(f"Loading compound list from {compound_file}...")
    compounds_df = pd.read_csv(compound_file)
    compounds = compounds_df["compound_name"].tolist()
    print(f"Loaded {len(compounds)} compounds.")
    return compounds_df, compounds


# Step 2: Load and filter data for specific metrics
def load_data(
    data_directory: str, compounds: list[str]
) -> tuple[dict[str, pd.DataFrame], dict[str, dict]]:
    """
    Load and filter the activity data for specific metrics (e.g., ED50, TD50) for each compound.

    Args:
        data_directory (str): The directory where the data files are located.
        compounds (list[str]): The list of compound names.

    Returns:
        tuple[dict[str, pd.DataFrame], dict[str, dict]]:
            A tuple containing two dictionaries:
            - The first dictionary maps compound names to their filtered data.
            - The second dictionary maps compound names to their properties.
    """
    print("Starting to load data for each compound...")
    metrics = ["ED50", "TD50"]
    data = {}
    properties = {}

    for compound in compounds:
        filepath = os.path.join(data_directory, f"{compound}_activity_data.csv")
        info_filepath = os.path.join("drug_info", f"{compound}_info.csv")
        if os.path.exists(filepath):
            print(f"Loading data for {compound} from {filepath}...")
            try:
                df = pd.read_csv(filepath)
                print(f"Data for {compound} loaded successfully, shape: {df.shape}")

                df_filtered = df[df["standard_type"].isin(metrics)]
                print(
                    f"Filtered data for {compound}, remaining rows: {len(df_filtered)}"
                )

                if not df_filtered.empty:
                    data[compound] = df_filtered
                    if os.path.exists(info_filepath):
                        properties[compound] = (
                            pd.read_csv(info_filepath).iloc[0].to_dict()
                        )
            except Exception as e:
                print(f"Error loading data for {compound}: {e}")
        else:
            print(f"File not found: {filepath}")

    print("Data loading completed.")
    return data, properties


# Create visualizations using Plotly Core Library
def create_visualizations(data: dict[str, pd.DataFrame]) -> dict[str, go.Figure]:
    """
    Create visualizations (scatter plots and box plots) for each compound's ED50 and TD50 data.

    Args:
        data (dict[str, pd.DataFrame]): The dictionary mapping compound names to their filtered data.

    Returns:
        dict[str, go.Figure]: A dictionary mapping compound names to their corresponding Plotly figures.
    """
    print("Starting to create visualizations...")
    figures = {}

    for compound, df in data.items():
        # Check if both ED50 and TD50 are present
        if all(metric in df["standard_type"].values for metric in ["ED50", "TD50"]):
            # Scatter plot of ED50 vs TD50 using Plotly core
            scatter_fig = go.Figure()

            for metric in ["ED50", "TD50"]:
                filtered_df = df[df["standard_type"] == metric]
                scatter_fig.add_trace(
                    go.Scatter(
                        x=filtered_df["standard_value"],
                        y=[metric] * len(filtered_df),
                        mode="markers",
                        marker=dict(
                            size=10,
                            color=(
                                "rgba(135, 206, 250, .9)"
                                if metric == "ED50"
                                else "rgba(255, 99, 71, .9)"
                            ),
                        ),
                        name=metric,
                        text=filtered_df[
                            "assay_description"
                        ],  # Include assay_description in hover text
                        hoverinfo="text+x+y",
                    )
                )

            scatter_fig.update_layout(
                title=f"{compound.capitalize()}: ED50 vs TD50 by Target Organism",
                xaxis_title="Standard Value (mg/kg)",
                yaxis_title="Measurement Type",
                yaxis=dict(tickmode="array", tickvals=["ED50", "TD50"]),
                hovermode="closest",
            )
            figures[f"{compound}_ed_td"] = scatter_fig
            print(f"ED50/TD50 scatter plot created for {compound}.")

            # Distribution plot for ED50 and TD50 using Plotly core
            box_fig = go.Figure()

            for metric in ["ED50", "TD50"]:
                filtered_df = df[df["standard_type"] == metric]
                box_fig.add_trace(
                    go.Box(
                        y=filtered_df["standard_value"],
                        x=[metric] * len(filtered_df),
                        name=metric,
                        boxpoints="all",  # show all points
                        jitter=0.3,
                        pointpos=-1.8,
                        marker=dict(
                            color=(
                                "rgba(135, 206, 250, .9)"
                                if metric == "ED50"
                                else "rgba(255, 99, 71, .9)"
                            )
                        ),
                        text=filtered_df[
                            "assay_description"
                        ],  # Include assay_description in hover text
                        hoverinfo="text+x+y",
                    )
                )

            box_fig.update_layout(
                title=f"{compound.capitalize()}: Distribution of ED50 and TD50",
                yaxis_title="Standard Value (mg/kg)",
                xaxis_title="Measurement Type",
                hovermode="closest",
            )
            figures[f"{compound}_distribution"] = box_fig
            print(f"ED50/TD50 distribution plot created for {compound}.")

    print("Visualizations created successfully.")
    return figures


# Create a Dash app
def create_dash_app(
    figures: dict[str, go.Figure],
    properties: dict[str, dict],
    data: dict[str, pd.DataFrame],
) -> dash.Dash:
    """
    Create a Dash app for visualizing compound data and their properties.

    Args:
        figures (dict[str, go.Figure]): A dictionary of figures for each compound.
        properties (dict[str, dict]): A dictionary of properties for each compound.
        data (dict[str, pd.DataFrame]): A dictionary of the compound data for the new page.

    Returns:
        dash.Dash: The Dash app instance.
    """
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    print("Initializing Dash app...")

    # Home page layout
    home_layout = html.Div(
        [
            html.H1(
                "Effective dose vs toxic dose for anticonvulsant drugs",
                style={"textAlign": "center", "margin-bottom": "20px"},
            ),
            dcc.Dropdown(
                id="compound-dropdown",
                options=[
                    {"label": f"{compound.capitalize()} - ED50 vs TD50", "value": key}
                    for key, compound in [
                        (key, key.split("_")[0]) for key in figures.keys()
                    ]
                ],
                value=list(figures.keys())[0] if figures else None,
                clearable=False,
                style={"width": "50%", "margin": "auto"},
            ),
            html.Div(
                id="drug-info", style={"textAlign": "center", "margin-top": "20px"}
            ),
            html.Hr(),  # Horizontal line separator
            html.Div(
                dcc.Link(
                    "Go to Organism Data",
                    href="/organisms",
                    style={
                        "display": "block",
                        "textAlign": "center",
                        "fontWeight": "bold",
                        "margin-top": "20px",
                    },
                )
            ),
            dcc.Graph(id="compound-graph"),
        ]
    )

    # New page layout for organism data
    organism_layout = html.Div(
        [
            html.H1(
                "Organisms and Test Frequencies by Drug",
                style={"textAlign": "center", "margin-bottom": "20px"},
            ),
            dcc.Link(
                "Go to Home Page",
                href="/",
                style={
                    "display": "block",
                    "textAlign": "center",
                    "margin-bottom": "20px",
                    "fontWeight": "bold",
                },
            ),
            html.Div(id="organism-data"),
            dcc.Graph(id="organism-bar-chart"),
        ]
    )

    app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content"),
        ]
    )

    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/organisms":
            return organism_layout
        else:
            return home_layout

    @app.callback(
        [Output("compound-graph", "figure"), Output("drug-info", "children")],
        [Input("compound-dropdown", "value")],
    )
    def update_graph(selected_compound: str):
        print(f"Updating graph for {selected_compound}")
        fig = figures[selected_compound]
        compound_name = selected_compound.split("_")[0]
        info = properties.get(compound_name, {})

        info_text = html.Div(
            [
                html.P(f"Drug: {info.get('Drug', 'N/A')}"),
                html.P(f"Molecular Formula: {info.get('Molecular Formula', 'N/A')}"),
                html.P(
                    f"Molecular Weight: {info.get('Molecular Weight', 'N/A')} g/mol"
                ),
                html.P(f"XLogP: {info.get('XLogP', 'N/A')}"),
                html.P(f"H-Bond Donor Count: {info.get('H-Bond Donor Count', 'N/A')}"),
                html.P(
                    f"H-Bond Acceptor Count: {info.get('H-Bond Acceptor Count', 'N/A')}"
                ),
                html.P(f"Exact Mass: {info.get('Exact Mass', 'N/A')} g/mol"),
                html.P(
                    f"Topological Polar Surface Area (TPSA): {info.get('Topological Polar Surface Area (TPSA)', 'N/A')} Å²"
                ),
            ]
        )

        return fig, info_text

    @app.callback(
        [Output("organism-data", "children"), Output("organism-bar-chart", "figure")],
        Input("url", "pathname"),
    )
    def display_organism_data(_):
        organism_data = []

        for compound, df in data.items():
            organism_counts = df["target_organism"].dropna().value_counts().to_dict()
            for organism, count in organism_counts.items():
                organism_data.append(
                    {
                        "Compound": compound.capitalize(),
                        "Organism": organism,
                        "Test Count": count,
                    }
                )

        organism_df = pd.DataFrame(organism_data)

        organism_table = dbc.Table.from_dataframe(
            organism_df,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
        )

        # Create a bar chart visualization
        bar_chart = go.Figure()
        for compound in organism_df["Compound"].unique():
            compound_df = organism_df[organism_df["Compound"] == compound]
            bar_chart.add_trace(
                go.Bar(
                    x=compound_df["Organism"],
                    y=compound_df["Test Count"],
                    name=compound,
                )
            )

        bar_chart.update_layout(
            title="Test Counts by Organism and Drug",
            xaxis_title="Organism",
            yaxis_title="Test Count",
            barmode="group",
            hovermode="closest",
        )

        return organism_table, bar_chart

    print("Dash app initialized successfully.")
    return app
