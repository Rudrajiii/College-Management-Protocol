import numpy as np
import pandas as pd


# Excel to json converting function
def convert_xlsx_to_json(file): 
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(file, engine='openpyxl')


    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna('')

    # Convert DataFrame to JSON
    json_data = df.to_dict(orient='records')

    return json_data
