import pandas as pd

def read_excel_to_dict(filepath, sheetname=0, header_row=0, drop_empty=True):
    df = pd.read_excel(filepath,
                       sheet_name=sheetname,
                       header=header_row)

    df.columns = df.columns.str.strip()
    if drop_empty:
        df.dropna(how='all', inplace=True)

    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient='records')
    return records
