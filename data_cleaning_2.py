import pandas as pd

def load_data(url):
    df = pd.read_csv(url)
    return df

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df = df.rename(columns={"st": "state"})
    return df

def clean_categorical_values(df):
    df["gender"] = df["gender"].replace({
        "Female": "F",
        "female": "F",
        "Male": "M",
        "male": "M"})

    df["state"] = df["state"].replace({
        "AZ": "Arizona",
        "WA": "Washington",
        "Cali": "California"})

    df["education"] = df["education"].replace({
        "Bachelors": "Bachelor"})

    df["vehicle_class"] = df["vehicle_class"].replace({
        "Sports Car": "Luxury",
        "Luxury SUV": "Luxury",
        "Luxury Car": "Luxury"})

    return df

def format_numeric_columns(df):
    df["customer_lifetime_value"] = (
        df["customer_lifetime_value"]
        .astype(str)  
        .str.replace("%", "")
        .astype(float))

    df["number_of_open_complaints"] = (
        df["number_of_open_complaints"]
        .astype(str)
        .str.split("/")
        .str[1]
        .astype(float))

    return df

def handle_nulls(df):
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        if col == "number_of_open_complaints":
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna(df[col].median())

    if "gender" in df.columns:
        df["gender"] = df["gender"].fillna("Unknown")


    categorical_cols = df.select_dtypes(include="object").columns
    categorical_cols = categorical_cols.drop("gender", errors="ignore")

    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
        
    return df

def handle_duplicates(df):
    df = df.drop_duplicates().reset_index(drop=True)
    return df
    
def main(url):
    df = load_data(url)
    df = clean_column_names(df)
    df = clean_categorical_values(df)
    df = format_numeric_columns(df)
    df = handle_nulls(df)
    df = handle_duplicates(df)
    return df
