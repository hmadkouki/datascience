import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter, HoverTool


def read_and_process_csv(file_paths, rename_columns, date_col=None, filters=None):
    data_frames = []
    for path in file_paths:
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(path, encoding="utf-16")
            except Exception as e:
                print(
                    f"Error processing {path} with both utf-8 and utf-16 encodings: {e}"
                )
                continue

        if rename_columns:
            df.rename(columns=rename_columns, inplace=True)
        if date_col and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])
        else:
            print(
                f"Column '{date_col}' not found in {path}. Please check the CSV structure."
            )

        for filter in filters or []:
            col, op, val = filter
            if col in df.columns:
                if op == "!=":
                    df = df[df[col] != val]
                elif op == ">":
                    df = df[df[col] > val]
            else:
                print(f"Column '{col}' for filtering not found in {path}.")

        data_frames.append(df)

    if not data_frames:
        print("No data frames were created. Please check the files and encodings.")
        return (
            pd.DataFrame()
        )  # Return an empty DataFrame to handle the concatenation issue gracefully.
    return pd.concat(data_frames, ignore_index=True)


# Define file paths
base_path = "data/"
sales_files = [f"data/sales_2021{month:02}.csv" for month in range(6, 11)]
crashes_files = [
    f"data/stats_crashes_2021{month:02}_overview.csv" for month in range(6, 13)
]

ratings_files = [
    f"data/stats_ratings_2021{month:02}_overview.csv" for month in range(6, 13)
]

# Define column mappings and filters
sales_columns = {
    "Transaction Date": "Transaction_date",
    "Transaction Type": "Transaction_type",
    "Product id": "Product_id",
    "Sku Id": "SKU_Id",
    "Buyer Country": "Buyer_country",
    "Buyer Postal Code": "Buyer_postalcode",
    "Amount (Merchant Currency)": "Amount",
}
crashes_columns = {
    "Date": "Date",
    "Package Name": "Package_name",
    "Daily Crashes": "Daily_stats_crashes",
    "Daily ANRs": "Daily_ANRS",
}

sales_filters = [("Transaction_type", "!=", "Google fee"), ("Amount", ">", 0)]

# Process files
sales_data = read_and_process_csv(
    sales_files, sales_columns, "Transaction_date", sales_filters
)
crashes_data = read_and_process_csv(crashes_files, crashes_columns, "Date")

# Data transformations for sales data
sales_data["Month"] = sales_data["Transaction_date"].dt.to_period("M").dt.to_timestamp()

# Aggregations
monthly_sales = sales_data.groupby("Month")["Amount"].sum().reset_index()
sku_sales_volume = sales_data.groupby("SKU_Id")["Amount"].sum().reset_index()
days_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
sales_data["Day_of_Week"] = pd.Categorical(
    sales_data["Transaction_date"].dt.day_name(), categories=days_order, ordered=True
)
day_sales_volume = sales_data.groupby("Day_of_Week")["Amount"].sum().reset_index()
country_sales_volume = sales_data.groupby("Buyer_country")["Amount"].sum().reset_index()

# Visualization
output_file("index.html")


def create_bar_chart(source, x, y, title, x_label, y_label, width=0.9):
    p = figure(
        title=title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        sizing_mode="scale_width",
    )
    # Set x_range dynamically if needed
    p.vbar(x=x, top=y, width=width, source=source)
    return p


def create_line_chart(source, x, y, title, x_label, y_label):
    p = figure(
        title=title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        x_axis_type="datetime",
        sizing_mode="scale_width",
    )
    p.line(x=x, y=y, source=source, color="red")
    p.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y")
    p.add_tools(
        HoverTool(
            tooltips=[(y, f"@{y}"), (x, f"@{x}{{%F}}")],
            formatters={f"@{x}": "datetime"},
        )
    )
    return p


# Ensure you convert SKU_Id and Day_of_Week to strings if they are not already
sales_data["SKU_Id"] = sales_data["SKU_Id"].astype(str)
sales_data["Day_of_Week"] = sales_data["Day_of_Week"].astype(str)

# Then create the ColumnDataSource objects
monthly_sales_source = ColumnDataSource(monthly_sales)
sku_sales_source = ColumnDataSource(sku_sales_volume)
day_sales_source = ColumnDataSource(day_sales_volume)
country_sales_source = ColumnDataSource(country_sales_volume)
crashes_source = ColumnDataSource(crashes_data)

print(monthly_sales.head())
print(sku_sales_volume.head())
print(day_sales_volume.head())
print(country_sales_volume.head())


# Make sure the x_range is a list of strings for SKU_Id and Day_of_Week
p_sku = create_bar_chart(
    sku_sales_volume,  # Data Frame, not ColumnDataSource
    "SKU_Id",
    "Amount",
    "Sales Volume per SKU Id",
    "SKU Id",
    "Sales Volume",
    width=0.9,
)

p_day = create_bar_chart(
    day_sales_volume,  # Data Frame, not ColumnDataSource
    "Day_of_Week",
    "Amount",
    "Sales Volume by Day of the Week",
    "Day of the Week",
    "Sales Volume",
    width=0.9,
)
p_country = create_bar_chart(
    country_sales_source,
    "Buyer_country",
    "Amount",
    "Sales Volume by Buyer Country",
    "Country",
    "Sales Volume",
)
p_crashes = create_line_chart(
    crashes_source,  # This should work now as crashes_source is defined
    "Date",
    "Daily_stats_crashes",
    "Crashes per day",
    "Date",
    "Crashes",
)
# Organize and show the layout
layout = gridplot([[p_sku, p_day], [p_country, p_crashes]], sizing_mode="scale_width")
show(layout)
