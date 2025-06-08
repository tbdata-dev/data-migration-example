import os

import pandas as pd
from sqlalchemy.inspection import inspect

from utils.logger import logger


def export_all_tables_to_csv(engine, output_dir="data/final_files"):

    os.makedirs(output_dir, exist_ok=True)

    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    for table_name in table_names:
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, engine)
            csv_path = os.path.join(output_dir, f"{table_name}.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Exported {table_name} to {csv_path}")
        except Exception as e:
            logger.error(f"Failed to export {table_name}: {e}")
