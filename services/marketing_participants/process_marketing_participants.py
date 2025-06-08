from utils.file import read_excel_to_dict
from utils.logger import logger
from services.marketing_participants.events import map_mp_row
from services.marketing_participants.shared import create_mp


# parse marketing participants from the events file
def process_mps_from_events(db, filepath: str):
    sheets = ["Leaders and Partners Dinner", "2019 Market Re-Cap"]

    logger.info(f"Processing contacts from {filepath} with sheets: {sheets}")

    processed_mps = []

    for sheet in sheets:
        logger.info(f"Processing sheet: {sheet}")
        records = read_excel_to_dict(filepath, sheetname=sheet, header_row=0, drop_empty=True)

        for row in records:
            try:
                mp_data = map_mp_row(db, row, sheet)
                logger.info(f'Row normalized to: {mp_data}')

                if mp_data:
                    new_mp = create_mp(db, mp_data)
                    processed_mps.append(new_mp)

            except Exception as e:
                logger.error(f"Error processing row {row} in {filepath}: {e}")
                continue

    return processed_mps
