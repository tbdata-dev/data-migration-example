import re

from utils.logger import logger
from utils.data import normalize_phone_number

# Split by common delimiters and strip whitespace
def split_field(value):
    if not value or not isinstance(value, str):
        return []
    value = value.replace(":", ";")
    return [v.strip() for v in re.split(r";|\n", value) if v.strip()]


# Extract name and company if in format "Name (Company)"
def extract_name_and_company(text):
    match = re.match(r"(.+?)\s*\((.+?)\)", text)
    if match:
        name, company = match.groups()
        return name.strip(), company.strip()
    return text.strip(), None


# Extract name, company, and email from given strings
def extract_name_and_company_emails(name_str, email_str, fallback_companies=None):
    if not name_str:
        return []

    fallback_companies = fallback_companies or []
    # Clean name to create email prefix
    name_clean = re.sub(r'\W+', '', name_str)
    contacts = []

    # If email is missing or invalid, use fallback companies without email
    if not email_str or '@' not in email_str:
        for company in fallback_companies:
            contacts.append((name_str.strip(), company.strip(), None))
        return contacts

    # Extract domain(s) from email string

    # split on @ and take the domain part
    local_part, domain_part = email_str.split('@', 1)

    # split on common delimiters and clean up (spaces, commas, .com)
    domains = [d.strip().lower().replace(" ", "").replace(",", "") for d in domain_part.replace(".com", "").split(",") if d.strip()]

    # If we have fallback companies, use them to create domains if counts don't match
    if fallback_companies and len(domains) != len(fallback_companies):
        domains = [c.lower().replace(" ", "") for c in fallback_companies]

    # loop through domains and create contacts
    for i, domain in enumerate(domains):
        company = fallback_companies[i] if i < len(fallback_companies) else domain
        email = f"{name_clean}@{domain}.com"
        contacts.append((name_str.strip(), company.strip(), email))

    return contacts



def map_contact_row_from_pipeline(row):
    logger.info(f"Mapping contact row: {row}")

    bankers_raw = split_field(row.get("Banker", ""))
    emails_raw = split_field(row.get("Banker Email", ""))
    phones_raw = split_field(row.get("Banker Phone Number", ""))
    default_company = row.get("Invest. Bank", "").strip() if row.get("Invest. Bank") else None

    contacts = []

    for i, banker in enumerate(bankers_raw):
        if not banker:
            continue

        name = banker.strip()
        raw_email = emails_raw[i] if i < len(emails_raw) else None
        raw_phone = phones_raw[i] if i < len(phones_raw) else None
        phone = normalize_phone_number(raw_phone)


        name, embedded_company = extract_name_and_company(name)
        fallback_companies = [c.strip() for c in embedded_company.split(",")] if embedded_company else [c.strip() for c in default_company.split(",") if c.strip()]

        name_company_email_triples = extract_name_and_company_emails(name, raw_email, fallback_companies)

        for person_name, company, email in name_company_email_triples:

            # Ignore company if it's a generic term
            if company in ['Direct to Company', 'Direct to FIS']:
                company = None

            contact = {
                "name": person_name,
                "company": company,
                "email": email.lower() if email else None,
                "phone": phone,
            }
            logger.info(f"Parsed banker contact: {contact}")
            contacts.append(contact)

    return contacts