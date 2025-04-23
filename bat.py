# load packages
import os
import pathlib
import zipfile

# third-party imports
import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

# make reproducible file paths
data_dir = os.path.join(
    pathlib.Path.home(), "earth-analytics", "data", "wildfire_wildlife"
)

# make the directory
os.makedirs(data_dir, exist_ok=True)

# hard coded fire boundary shapefile from mtbs.gov/direct-download
fb_zip_path = os.path.join(data_dir, "co4020310623920201014.zip")

# unzip file
fb_dir = os.path.join(data_dir, "co4020310623920201014")
if not os.path.exists(fb_dir):
    with zipfile.ZipFile(fb_zip_path, "r") as zip_ref:
        zip_ref.extractall(fb_dir)
    print(f"Extracted data to {fb_dir} directory")

# open fb path
fb_path = os.path.join(fb_dir, "co4020310623920201014_20200904_20210907_burn_bndy.shp")

# open polygon
fb_shp = gpd.read_file(fb_path)

# Reproject GeoDataFrame to the same CRS as the basemap
# (Web Mercator, EPSG:3857)
fb_shp_merc = fb_shp.to_crs(epsg=3857)

# Create a plot
ax = fb_shp_merc.plot(
        figsize=(10, 10), 
        facecolor="none",
        edgecolor="red",
        linewidth=2
        )
ctx.add_basemap(
    ax,
    crs=fb_shp_merc.crs.to_string(),
    source=ctx.providers.Esri.WorldImagery,
)
plt.title("East Troublesome Fire (2020) Boundary")
ax.set_xlabel("X (meters)")
ax.set_ylabel("Y (meters)")

# Show the plot
# plt.show()
# open site data path
sd_path = os.path.join(data_dir, "Site_Data.csv")

# open site data
sd = pd.read_csv(sd_path)
# set column names to lowercase
sd.columns = sd.columns.str.lower()
# filter out unnecessary columns
sd = sd[['site', 'lattitude', 'longitude']]
# filter out all rows except East Troublesome fire 
sd = sd[sd['site'].str.contains('et', case=False)]

# pad site numbers to all have 3 digits
sd['site'] = sd['site'].str.replace(r'(\d+)', lambda x: x.group(1).zfill(3), regex=True)

# open bat data path
bd_path = os.path.join(data_dir, "COFires_bats_2024.csv")

# open bat data
bd = pd.read_csv(bd_path)
# set column names to lowercase
bd.columns = bd.columns.str.lower()
# filtern out unncessary columns
bd = bd[['site', 'hi_pass', 'lo_pass', 'area']]
# filter out all rows except East Troublesome fire
bd = bd[bd['site'].str.contains('et', case=False)]
# Fix bat site names by removing the fire severity after the fire prefix
bd['site'] = bd['site'].str.replace(r'^([A-Z]{2})[1-4]-', r'\1-', regex=True)
# pad site numbers to all have 3 digits
bd['site'] = bd['site'].str.replace(r'(\d+)', lambda x: x.group(1).zfill(3), regex=True)

# merge datasets on the 'site' column
combined_df = sd.merge(bd, on='site')

# Extract numeric part from 'area' and rename to 'burn_severity'
combined_df['burn_severity'] = combined_df['area'].str.extract(r'(\d+)').astype(int)
combined_df.drop(columns='area', inplace=True)

# rename hi_pass and lo_pass for readability
combined_df.rename(columns={
    'hi_pass': 'high_frequency',
    'lo_pass': 'low_frequency'
}, inplace=True)

# sum high and low values for each site
summary_df = combined_df.groupby('site').agg({
    'lattitude': 'first',
    'longitude': 'first',
    'high_frequency': 'sum',
    'low_frequency': 'sum',
    'burn_severity': 'first'
}).reset_index()

# Melt the summary_df so hi_pass and lo_pass become one column
melted = summary_df.melt(
    id_vars='burn_severity',
    value_vars=['high_frequency', 'low_frequency'],
    var_name='Call Type',
    value_name='Call Count'
)

# Plot
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

sns.boxplot(
    data=melted,
    x='burn_severity',
    y='Call Count',
    hue='Call Type',
    palette='muted',
)
plt.title('Bat Activity vs Burn Severity')
plt.xlabel("Burn Severity")
plt.ylabel("Total Call Count")
plt.legend(title="Call Type")
plt.tight_layout()
plt.show()

def plot_bat_activity_by_severity(summary_df, response_col):
    """
    Fit a Negative Binomial model and plot predicted bat activity by burn severity.

    Parameters:
        summary_df (pd.DataFrame): Dataframe with columns ['burn_severity', response_col]
        response_col (str): Either 'lo_pass' or 'hi_pass'
    """
    # Ensure burn_severity is categorical
    summary_df = summary_df.copy()
    summary_df['burn_severity'] = pd.Categorical(summary_df['burn_severity'])

    # Fit the model
    formula = f'{response_col} ~ C(burn_severity)'
    model = smf.glm(
        formula=formula,
        data=summary_df,
        family=sm.families.NegativeBinomial()
    ).fit()

    print(model.summary())

    # Prediction DataFrame using only available categories
    available_levels = summary_df['burn_severity'].cat.categories
    predict_df = pd.DataFrame({'burn_severity': available_levels})
    predict_df['burn_severity'] = pd.Categorical(
        predict_df['burn_severity'],
        categories=available_levels
    )

    # Predict response
    predict_df['predicted_calls'] = model.predict(predict_df)

    # Plot
    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=predict_df,
        x='burn_severity',
        y='predicted_calls',
        palette='viridis'
    )
    plt.xlabel("Burn Severity Level")
    plt.ylabel(f"Predicted Bat Activity ({response_col})")
    plt.title(f"Predicted Bat Activity by Burn Severity ({response_col})")
    plt.tight_layout()
    plt.show()

plot_bat_activity_by_severity(summary_df, 'high_frequency')
plot_bat_activity_by_severity(summary_df, 'low_frequency')

