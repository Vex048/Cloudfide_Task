
import pandas as pd
import re
allowed_characters = r"[a-zA-Z_]+"
role_check = r"[^a-zA-Z_\s\+\-\*]"
new_column_check = r"^[a-zA-Z_]+$"

# Function does check if new_column has correct characters (letters and underscores)
# Also it checks if there are correct characters in role
def check_if_columns_correct(role: str, new_column:str) -> bool:
    if not re.fullmatch(pattern=new_column_check, string=new_column):
        return False
    if re.search(pattern=role_check, string=role):
        return False
    return True

# Creates a copy of df, changes any occurrences of new lines and tabs
# Then does .eval() on dataframe from pandas library
def data_manipulation(df: pd.DataFrame,role:str,new_column : str) -> pd.DataFrame:
    df_result = df.copy()
    role_fixed = role.replace('\n', " ").replace('\t', " ").strip()
    try:
        df_result[new_column] = df_result.eval(role_fixed)
    except SyntaxError as e: # Case when the .eval() raise an SyntaxError, because of role_fixed which do some string manipulation
        print("Syntax Error during the .eval function")
        return pd.DataFrame([])
    return df_result

# Main function
def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    if not check_if_columns_correct(role, new_column):
        return pd.DataFrame([])

    columns = re.findall(allowed_characters, role)
    set_columns = set(columns)
    # Check if found columns using regex are in the df columns
    if not set_columns.issubset(df.columns):
        return pd.DataFrame([])
    return data_manipulation(df=df,role=role, new_column=new_column)