import pandas as pd
import io
from backend import database


def importData():
    df = pd.read_excel("data.xlsx")
    print(df)
    """
    clean data and insert into db
    database.create_doctor()
    database.create_appointment()
    database.create_nurse()
    database.create_patient()
    """


# Function to validate data
def validate_data(df):
    errors = []
    for index, row in df.iterrows():
        # Check for missing 'name'
        if pd.isna(row["name"]):
            errors.append(f"Row {index + 1}: Missing name")
        
        # Check for invalid 'age' (negative or non-numeric)
        if not isinstance(row["age"], (int, float)) or row["age"] < 0:
            errors.append(f"Row {index + 1}: Invalid age")
        
        # Add more checks for other columns as needed (e.g., medical history)

    return errors


def handle_errors(errors):
    with open("errors.log", "w") as log_file:
        for error in errors:
            log_file.write(error + "\n")


def clean_data(df):
    # Remove leading/trailing whitespaces and normalize text for 'name'
    df["name"] = df["name"].str.strip().str.title()
    
    # Handle duplicates
    df = df.drop_duplicates()

    return df





