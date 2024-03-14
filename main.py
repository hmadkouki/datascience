import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot, column
from bokeh.models import (
    DatetimeTickFormatter,
    HoverTool,
    GeoJSONDataSource,
    LinearColorMapper,
    ColorBar,
)
import geopandas as gpd
from bokeh.palettes import Viridis6 as palette, brewer
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.tile_providers import get_provider


def add_column_data(existing_df, custom_df, column_name, custom_column_name):
    """
    Add data from a specified column of an existing DataFrame to a specified column
    of a custom DataFrame without overwriting existing data.

    Parameters:
        existing_df (DataFrame): Existing DataFrame containing data.
        custom_df (DataFrame): Custom DataFrame to which data will be added.
        column_name (str): Name of the column in the existing DataFrame from which data will be extracted.
        custom_column_name (str): Name of the column in the custom DataFrame to which data will be added.
    """
    custom_df[custom_column_name] = custom_df.get(
        custom_column_name, pd.Series()
    ).append(existing_df[column_name], ignore_index=True)


list_csv = [
    "sales_202106.csv",
    "sales_202107.csv",
    "sales_202108.csv",
    "sales_202109.csv",
    "sales_202110.csv",
]
# create a second list and store the csv's in the list. The csv's are in 'data' directory
list_csv = [f"data/{csv}" for csv in list_csv]
list_columns_new = [
    "Transaction_date",
    "Transaction_type",
    "Product_id",
    "SKU_Id",
    "Buyer_country",
    "Buyer_postalcode",
    "Amount",
]
list_columns_old = [
    "Transaction Date",
    "Transaction Type",
    "Product id",
    "Sku Id",
    "Buyer Country",
    "Buyer Postal Code",
    "Amount (Merchant Currency)",
]

# Define your custom DataFrame
sales_main = pd.DataFrame(
    {
        "Transaction_date": [],
        "Transaction_type": [],
        "Product_id": [],
        "SKU_Id": [],
        "Buyer_country": [],
        "Buyer_postalcode": [],
        "Amount": [],
    }
)


def add_column_data(existing_df, custom_df):
    return pd.concat([custom_df, existing_df], ignore_index=True)


for csv_file in list_csv:
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file)

    # Rename columns to match custom DataFrame
    df.rename(columns=dict(zip(list_columns_old, list_columns_new)), inplace=True)

    # Add data from the current DataFrame to the custom DataFrame
    sales_main = add_column_data(df, sales_main)

# Display updated sales_main DataFrame

sales_df = sales_main[list_columns_new].copy()

# convet the Transaction_date to datetime
sales_df["Transaction_date"] = pd.to_datetime(sales_df["Transaction_date"])
# delete all rows with Transaction_type == 'Google fee'
sales_df = sales_df[sales_df["Transaction_type"] != "Google fee"]
# only show transactions with amount > 0
sales_df = sales_df[sales_df["Amount"] > 0]


#### 2nd part of the code, crashes data

list_csv_stats_crashes = [
    "stats_crashes_202106_overview.csv",
    "stats_crashes_202107_overview.csv",
    "stats_crashes_202108_overview.csv",
    "stats_crashes_202109_overview.csv",
    "stats_crashes_202110_overview.csv",
    "stats_crashes_202111_overview.csv",
    "stats_crashes_202112_overview.csv",
]

list_csv_stats_crashes = [f"data/{csv}" for csv in list_csv_stats_crashes]
list_columns_new_stats_crashes = [
    "Date",
    "Package_name",
    "Daily_stats_crashes",
    "Daily_ANRS",
]

list_columns_old_stats_crashes = ["Date", "Package Name", "Daily Crashes", "Daily ANRs"]

# Define your custom DataFrame
crashes_main = pd.DataFrame(
    {"Date": [], "Package_name": [], "Daily_stats_crashes": [], "Daily_ANRS": []}
)
for csv_file in list_csv_stats_crashes:
    try:
        df = pd.read_csv(csv_file, encoding="utf-16")  # Adjust the encoding here
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(
                csv_file, encoding="iso-8859-1"
            )  # Try a different encoding if utf-16 fails
        except Exception as e:
            print(f"Failed to read {csv_file} with multiple encodings: {e}")
            continue

    # Rename columns to match custom DataFrame
    df.rename(
        columns=dict(
            zip(list_columns_old_stats_crashes, list_columns_new_stats_crashes)
        ),
        inplace=True,
    )

    # Add data from the current DataFrame to the custom DataFrame
    crashes_main = add_column_data(df, crashes_main)
    # date to datetime
    crashes_main["Date"] = pd.to_datetime(crashes_main["Date"])

# 3rd part of the code ratings data
list_csv_stats_ratings = [
    "stats_ratings_202106_country.csv",
    "stats_ratings_202107_country.csv",
    "stats_ratings_202108_country.csv",
    "stats_ratings_202109_country.csv",
    "stats_ratings_202110_country.csv",
    "stats_ratings_202111_country.csv",
    "stats_ratings_202112_country.csv",
]

list_csv_stats_ratings = [f"data/{csv}" for csv in list_csv_stats_ratings]
list_columns_new_stats_ratings = [
    "Date",
    "Package_name",
    "Country",
    "Daily_average_rating",
    "Total_average_rating",
]

list_columns_old_stats_ratings = [
    "Date",
    "Package Name",
    "Country",
    "Daily Average Rating",
    "Total Average Rating",
]

# Define your custom DataFrame
ratings_main = pd.DataFrame(
    {
        "Date": [],
        "Package_name": [],
        "Country": [],
        "Daily_average_rating": [],
        "Total_average_rating": [],
    }
)
for csv_file in list_csv_stats_ratings:
    try:
        df = pd.read_csv(csv_file, encoding="utf-16")  # Adjust the encoding here
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(
                csv_file, encoding="iso-8859-1"
            )  # Try a different encoding if utf-16 fails
        except Exception as e:
            print(f"Failed to read {csv_file} with multiple encodings: {e}")
            continue

    # Rename columns to match custom DataFrame
    df.rename(
        columns=dict(
            zip(list_columns_old_stats_ratings, list_columns_new_stats_ratings)
        ),
        inplace=True,
    )

    # Add data from the current DataFrame to the custom DataFrame
    ratings_main = add_column_data(df, ratings_main)
    # date to datetime
    ratings_main["Date"] = pd.to_datetime(ratings_main["Date"])

# delete all the nan values from ratings_main
ratings_main = ratings_main.dropna()
# create a ratings dataframe grouped by country
ratings_country = (
    ratings_main.groupby("Country")["Daily_average_rating"].mean().reset_index()
)

# create a barcahrt with the ratings per country export to html
output_file("ratings_country.html")
source = ColumnDataSource(ratings_country)
p = figure(
    x_range=ratings_country["Country"].tolist(),
    title="Average rating per country",
    x_axis_label="Country",
    y_axis_label="Average rating",
    sizing_mode="inherit",
    toolbar_location=None,
)
p.vbar(x="Country", top="Daily_average_rating", width=0.9, source=source)
p.xaxis.major_label_orientation = 1
show(p)


# plot the rating and date in a bokeh plot
# Create a new plot with a datetime axis type
source_rating = ColumnDataSource(ratings_main)
p = figure(
    x_axis_type="datetime",
    title="Rating per day",
    x_axis_label="Date",
    y_axis_label="Rating",
    sizing_mode="inherit",
)
p.line(
    x="Date",
    y="Daily_average_rating",
    source=source_rating,
    legend_label="Rating",
    color="blue",
)
p.line(
    x="Date",
    y="Total_average_rating",
    source=source_rating,
    legend_label="Total Average Rating",
    color="green",
)
p.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y")
p.add_tools(
    HoverTool(
        tooltips=[("Rating", "@rating"), ("Date", "@Date{%F}")],
        formatters={"@Date": "datetime"},
    )
)
output_file("ratings.html")
show(p)

# use bokeh to plot the sales_df dataframe data and export the plot as a html file
# visualize the crashes data per day in the same html file
output_file("index.html")
source = ColumnDataSource(sales_df)
source2 = ColumnDataSource(crashes_main)

# create new df for usage with geopandas and to visualize buyers per country
sales_df_country = sales_df.groupby("Buyer_country")["Amount"].sum().reset_index()

# Group by month and sum the amounts
sales_df["Month"] = sales_df["Transaction_date"].dt.to_period("M")
monthly_sales = sales_df.groupby("Month")["Amount"].sum().reset_index()

# Convert 'Month' to datetime to be compatible with Bokeh's datetime x-axis
monthly_sales["Month"] = monthly_sales["Month"].dt.to_timestamp()

# Update the ColumnDataSource for the sales data
source = ColumnDataSource(monthly_sales)

# Assuming sales_df is already created and preprocessed as per your previous code

# Add new columns for segmentation
sales_df["Day_of_Week"] = sales_df["Transaction_date"].dt.day_name()
sales_df["Time_of_Day"] = sales_df[
    "Transaction_date"
].dt.hour  # This assumes you have time in your 'Transaction_date'

# Group by SKU Id and sum the Amounts
sku_sales_volume = sales_df.groupby("SKU_Id")["Amount"].sum().reset_index()
day_sales_volume = sales_df.groupby("Day_of_Week")["Amount"].sum().reset_index()
country_sales_volume = sales_df.groupby("Buyer_country")["Amount"].sum().reset_index()

# Sort the 'day_sales_volume' by the day of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_sales_volume["Day_of_Week"] = pd.Categorical(
    day_sales_volume["Day_of_Week"], categories=days, ordered=True
)
day_sales_volume = day_sales_volume.sort_values("Day_of_Week")

# Prepare the data source for Bokeh
sku_source = ColumnDataSource(sku_sales_volume)
day_source = ColumnDataSource(day_sales_volume)
country_source = ColumnDataSource(country_sales_volume)

# Output file
# Begin plotting
output_file("index.html")

# Group by SKU Id and sum the Amounts
sku_sales_volume = sales_df.groupby("SKU_Id")["Amount"].sum().reset_index()
day_sales_volume = sales_df.groupby("Day_of_Week")["Amount"].sum().reset_index()
country_sales_volume = sales_df.groupby("Buyer_country")["Amount"].sum().reset_index()

# Sort the 'day_sales_volume' by the day of the week
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_sales_volume["Day_of_Week"] = pd.Categorical(
    day_sales_volume["Day_of_Week"], categories=days, ordered=True
)
day_sales_volume = day_sales_volume.sort_values("Day_of_Week")

# Prepare the data source for Bokeh
sku_source = ColumnDataSource(sku_sales_volume)
day_source = ColumnDataSource(day_sales_volume)
country_source = ColumnDataSource(country_sales_volume)

output_file("sales_volume_per_sku.html")  # Specify unique filename here
# Configure the bar plots
p_sku = figure(
    x_range=sku_sales_volume["SKU_Id"].tolist(),
    title="Sales Volume per SKU Id",
    x_axis_label="SKU Id",
    y_axis_label="Sales Volume",
    sizing_mode="inherit",
)
p_sku.vbar(x="SKU_Id", top="Amount", width=0.9, source=sku_source)
show(p_sku)

output_file("sales_volume_per_day.html")  # Specify unique filename here
p_day = figure(
    x_range=days,
    title="Sales Volume by Day of the Week",
    x_axis_label="Day of the Week",
    y_axis_label="Sales Volume",
    sizing_mode="inherit",
)
p_day.vbar(x="Day_of_Week", top="Amount", width=0.9, source=day_source)
show(p_day)

output_file("sales_volume_per_country.html")  # Specify unique filename here
# use geopandas to plot the sales volume per country
# Configure the bar plot for sales volume per country
p_country = figure(
    x_range=country_sales_volume["Buyer_country"].tolist(),
    title="Sales Volume per Country",
    x_axis_label="Country",
    y_axis_label="Sales Volume",
    sizing_mode="inherit",
    toolbar_location=None,
)
p_country.vbar(x="Buyer_country", top="Amount", width=0.9, source=country_source)
p_country.xaxis.major_label_orientation = 1
show(p_country)


# Configure the line plot for crashes
output_file("crashes_per_day.html")  # Specify unique filename here
p_crashes = figure(
    title="Crashes per day",
    x_axis_label="Date",
    y_axis_label="Crashes",
    x_axis_type="datetime",
    sizing_mode="inherit",
)
p_crashes.line(
    x="Date",
    y="Daily_stats_crashes",
    source=source2,
    legend_label="Crashes",
    color="red",
)
p_crashes.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y")
p_crashes.add_tools(
    HoverTool(
        tooltips=[("Crashes", "@Daily_stats_crashes"), ("Date", "@Date{%F}")],
        formatters={"@Date": "datetime"},
    )
)
show(p_crashes)


# Load a GeoDataFrame with world data
world = gpd.read_file("shapefile/ne_110m_admin_0_countries.shp")

# use geopandas to plot the sales volume per country
# Merge the GeoDataFrame with the sales volume per country
# Load a GeoDataFrame with world data (make sure to have the 'naturalearth_lowres' dataset downloaded)
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# Merge the GeoDataFrame with the DataFrame on the 'iso_a3' column, which contains the country codes
merged = world.merge(
    sales_df_country, how="left", left_on="iso_a3", right_on="Buyer_country"
)
merged["Amount"] = merged["Amount"].fillna(
    0
)  # Replace NaN with 0 for countries with no data

# Convert to GeoJSON format for Bokeh
geo_source = GeoJSONDataSource(geojson=merged.to_json())

# Define color mapper - this will map the 'Amount' values to colors
mapper = LinearColorMapper(
    palette=brewer["YlGnBu"][8],
    low=merged["Amount"].min(),
    high=merged["Amount"].max(),
    nan_color="#d9d9d9",
)

# Define color bar
color_bar = ColorBar(
    color_mapper=mapper,
    label_standoff=8,
    width=500,
    height=20,
    border_line_color=None,
    location=(0, 0),
    orientation="horizontal",
)

# Create figure
p = figure(
    title="Sales Amount by Country",
    x_axis_location=None,
    y_axis_location=None,
    tooltips=[("Country", "@iso_a3"), ("Amount", "@Amount")],
)

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

# Add patch renderer to figure
p.patches(
    "xs",
    "ys",
    source=geo_source,
    fill_color={"field": "Amount", "transform": mapper},
    line_color="black",
    line_width=0.25,
    fill_alpha=1,
)

# Add the color bar to the figure
p.add_layout(color_bar, "below")

# Output to HTML
output_file("sales_per_country.html")
show(column(p))
