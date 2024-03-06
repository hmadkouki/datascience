# use packages
import bokeh
import pandas as pd
import numpy as np
import os


class CSVFile:
    def __init__(self, filename):
        self.filename = filename
        self.filepath = os.path.join("data", filename)
        self.df = None

    def load(self, encoding="utf-8"):
        """Load the CSV file into a pandas DataFrame."""
        if os.path.exists(self.filepath):
            try:
                self.df = pd.read_csv(self.filepath, encoding=encoding)
            except UnicodeDecodeError as e:
                print(f"Failed to decode using {encoding}. Trying with 'utf-8-sig'.")
                self.df = pd.read_csv(self.filepath, encoding="utf-8-sig")
        else:
            raise FileNotFoundError(f"{self.filepath} does not exist.")

    def get_dataframe(self):
        """Return the loaded DataFrame."""
        if self.df is not None:
            return self.df
        else:
            print(
                "Dataframe is empty. Use the load() method to load data from the CSV file."
            )
            return None


# csv_instance = CSVFile(
#     "sales_202110.csv"
# )  # 'example.csv' is the name of your CSV file within the 'data' folder
# csv_instance.load(encoding="utf-8")  # Load the data from the CSV file
# df = csv_instance.get_dataframe()  # Get the DataFrame
# # print the column names


# # get the column Transaction Date and convert it to datetime
# df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
# print(df["Transaction Date"])


# for all csv files starting with sales_ in the data folder combine them into one dataframes
def combine_csv_files():
    csv_files = [file for file in os.listdir("data") if file.startswith("sales_")]
    print(csv_files)
    dataframes = []
    for file in csv_files:
        csv_instance = CSVFile(file)
        csv_instance.load()
        dataframes.append(csv_instance.get_dataframe())
    combined_df = pd.concat(dataframes, ignore_index=False)
    return combined_df


df = combine_csv_files()
list_of_columns = df.columns.tolist()
