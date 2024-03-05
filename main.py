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

    # write a function transforming the 'transaction_date' column to datetime and delete the original column
    def transform_date(self):
        self.df["transaction_date"] = pd.to_datetime(self.df["transaction_date"])
        return self.df


csv_instance = CSVFile(
    "sales_202110.csv"
)  # 'example.csv' is the name of your CSV file within the 'data' folder
csv_instance.load(encoding="utf-8")  # Load the data from the CSV file
df = csv_instance.get_dataframe()  # Get the DataFrame
# print the column names
print(df.head())

# print the type of the column
print(df.dtypes)
