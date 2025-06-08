from utils.logger import logger
import re


def map_pipeline_row(row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping pipeline row: {row}")

    return {
        'name': row.get('Company Name').strip() if row.get('Company Name') else None,
        'sectors': normalize_pipeline_sectors(row.get('Vertical'), row.get('Sub Vertical')),
        'description': row.get('Business Description').strip() if row.get('Business Description') else None,
        'company_type': 'Deal Target'
    }


def map_pipeline_row_bank(row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping pipeline row for bank: {row}")

    bank_list = []

    banks = parse_investment_banks(row.get('Invest. Bank'))
    for bank in banks:
        if not bank:
            logger.warning("Empty investment bank name found, skipping.")
            continue

        bank_list.append({'name': bank.strip()})
    return bank_list


# Normalize and combine vertical and subvertical into a single string
def normalize_pipeline_sectors(vertical, subvertical):
    sectors = []
    if vertical and isinstance(vertical, str):
        sectors.append(vertical.strip())
    if subvertical and isinstance(subvertical, str):
        sectors.append(subvertical.strip())
    return '; '.join(sectors) if sectors else None


# Parse investment banks from a string, handling various delimiters
def parse_investment_banks(value):

    if not value or not isinstance(value, str):
        return []

    normalized = re.sub(r"[\/;\n]", ",", value)

    banks = [b.strip() for b in normalized.split(",") if b.strip()]

    return banks