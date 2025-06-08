from utils.file import read_excel_to_dict
from utils.logger import logger
from services.deals.pipelines import map_deal_row
from services.deals.shared import create_deal

# process deals from either pipeline file
def process_deals_from_pipeline(db, filepath: str):
    if filepath == 'data/original_files/Consumer Retail and Healthcare Pipeline.xlsx':
        header_row = 8
    else:
        header_row = 5

    records = read_excel_to_dict(filepath, sheetname=0, header_row=header_row, drop_empty=True)
    processed_contacts = []

    for row in records:
        try:
            deal_row = map_deal_row(db, row)

            create_deal(db, deal_row)

        except Exception as e:
            logger.error(f"Error processing row {row} in {filepath}: {e}")
            continue

    return processed_contacts