import math
import re
from datetime import datetime

import pandas as pd

from services.companies.shared import check_company_exists
from services.contacts.pipelines import map_contact_row_from_pipeline
from services.contacts.shared import check_contact_exists
from utils.logger import logger


# normalize date that can be in format "Jan-23" or "Jan-2023"
def normalize_date(date_val):
    if pd.isna(date_val):
        return None
    if isinstance(date_val, str):
        for fmt in ("%b-%y", "%b-%Y"):
            try:
                return datetime.strptime(date_val, fmt)
            except ValueError:
                continue
        return None
    return date_val


# normalize float that can be in format "12,345.67" or "12.34"
def normalize_float(val):
    try:
        if val is None or (isinstance(val, str) and val.strip() == ''):
            return None
        val = float(val)
        if math.isnan(val):
            return None
        return val
    except (ValueError, TypeError):
        logger.warning(f"Could not convert to float: {val}")
        return None


def map_deal_row(db, row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping deal row: {row}")

    company_name = row.get('Company Name')
    company = check_company_exists(db, company_name)

    # Parse contacts
    banker_contacts = map_contact_row_from_pipeline(row)
    logger.info(f"Parsed banker contacts: {banker_contacts}")
    contact_ids = []
    for contact in banker_contacts:
        logger.info(f"Processing contact: {contact}")
        contact_company = check_company_exists(db, contact['company'])
        logger.info(f"Found contact company: {contact_company}")
        contact['company_id'] = contact_company.id if contact_company else None
        logger.info(f"Company ID set to: {contact['company_id']}")
        match = check_contact_exists(db, contact['email'], contact['name'], contact['company'])
        if match:
            contact_ids.append(str(match.id))

    # Parse investment bank companies
    banks_raw = row.get("Invest. Bank") or ""

    # Split by common delimiters and strip whitespace
    bank_names = [
        str(b).strip() for b in re.split(r"[;/,\n]", banks_raw)
        if b is not None and str(b).strip() != ''
    ]

    bank_ids = []

    for bank_name in bank_names:
        bank = check_company_exists(db, bank_name)
        if bank:
            bank_ids.append(str(bank.id))


    return {
        'company_id': company.id if company else None,
        'project_name': row.get('Project Name'),
        'date_added': normalize_date(row.get('Date Added')),
        'sourcing': row.get('Sourcing'),
        'transaction_type': row.get('Transaction Type'),
        'ltm_revenue': normalize_float(row.get('LTM Revenue')),
        'ltm_ebitda': normalize_float(row.get('LTM EBITDA')),
        'enterprise_value': normalize_float(row.get('Enterprise Value')),
        'estimated_equity_investment': normalize_float(row.get('Est. Equity Investment')),
        'status': row.get('Status'),
        'portfolio_company_status': row.get('Portfolio Company Status'),
        'active_stage': row.get('Active Stage'),
        'passed_rationale': row.get('Passed Rationale'),
        'current_owner': row.get('Current Owner'),
        'business_description': row.get('Business Description'),
        'lead_md': row.get('Lead MD'),
        'banker_contact_ids': "; ".join([str(cid) for cid in contact_ids]) if contact_ids else None,
        'investment_banks': "; ".join([str(bid) for bid in bank_ids]) if bank_ids else None,
    }
