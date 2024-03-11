import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter, HoverTool


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


##### 2nd part of the code, crashes data

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


# use bokeh to plot the sales_df dataframe data and export the plot as a html file
# visualize the crashes data per day in the same html file
output_file("index.html")
source = ColumnDataSource(sales_df)
source2 = ColumnDataSource(crashes_main)

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

# Configure the bar plots
p_sku = figure(
    x_range=sku_sales_volume["SKU_Id"].tolist(),
    title="Sales Volume per SKU Id",
    x_axis_label="SKU Id",
    y_axis_label="Sales Volume",
    sizing_mode="scale_width",
)
p_sku.vbar(x="SKU_Id", top="Amount", width=0.9, source=sku_source)

p_day = figure(
    x_range=days,
    title="Sales Volume by Day of the Week",
    x_axis_label="Day of the Week",
    y_axis_label="Sales Volume",
    sizing_mode="scale_width",
)
p_day.vbar(x="Day_of_Week", top="Amount", width=0.9, source=day_source)

p_country = figure(
    x_range=country_sales_volume["Buyer_country"].tolist(),
    title="Sales Volume by Buyer Country",
    x_axis_label="Country",
    y_axis_label="Sales Volume",
    sizing_mode="scale_width",
)
p_country.vbar(x="Buyer_country", top="Amount", width=0.9, source=country_source)

# Configure the line plot for crashes
p_crashes = figure(
    title="Crashes per day",
    x_axis_label="Date",
    y_axis_label="Crashes",
    x_axis_type="datetime",
    sizing_mode="scale_width",
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

# Organize the plots into a grid layout
layout = gridplot([[p_sku, p_day], [p_country, p_crashes]], sizing_mode="scale_width")

# Show the layout
show(layout)
