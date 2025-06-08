from utils.logger import logger


def map_contact_row_from_events(row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping events row: {row}")

    return {
        'name': row.get('Name').strip() if row.get('Name') else None,
        'email': row.get('E-mail').strip().lower() if row.get('E-mail') else None,
    }
