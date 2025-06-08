from utils.logger import logger


def map_pe_comps_row(row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None
    logger.info(f"Mapping PE comps row: {row}")

    return {
        'name': row.get('Company Name').strip(),
        'priority': row.get('Priority'),
        'website': row.get('Website'),
        'aum': normalize_aum(row.get('AUM\n(Bns)')),
        'sectors': normalize_multiline_fields(row.get('Sectors')),
        'company_type': 'PE Firm',
        'sample_portfolio_companies': normalize_multiline_fields(row.get('Sample Portfolio Companies')),
        'comments': normalize_multiline_fields(row.get('Comments')),
    }

# normalize text fields from multiple lines with '- ' prefix to a ';' separated string
def normalize_multiline_fields(sectors):
    if not sectors or not isinstance(sectors, str):
        return None

    parts = sectors.split('\n- ')

    parts[0] = parts[0].lstrip('- ').strip()

    return '; '.join(part.strip() for part in parts if part.strip())


# normalize AUM to integer in billions
def normalize_aum(aum):
    try:
        if aum is None or aum == '':
            return None
        return int(float(aum) * 1_000_000_000)
    except ValueError:
        logger.error(f'Invalid AUM value: {aum}')
        return None