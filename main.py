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


csv_instance = CSVFile(
    "reviews_202109.csv"
)  # 'example.csv' is the name of your CSV file within the 'data' folder
csv_instance.load(encoding="utf-16")  # Load the data from the CSV file
df = csv_instance.get_dataframe()  # Get the DataFrame
print(df)  # Print the DataFrame
