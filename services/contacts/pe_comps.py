import re

import phonenumbers

from utils.logger import logger


def map_contact_row_from_pe_comps(row):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping contact row: {row}")

    name, title, email, phone = parse_contact_block(row.get('Contact Name 1'))

    contacts = []
    if name:
        contacts.append({
            'name': name,
            'company': row.get('Company Name'),
            'title': title,
            'email': email,
            'phone': phone,
        })

    name, title, email, phone = parse_contact_block(row.get('Contact 2'))
    if name:
        contacts.append({
            'name': name,
            'company': row.get('Company Name'),
            'title': title,
            'email': email,
            'phone': phone,
        })

    return contacts


# Normalize text fields from multiple lines with '- ' prefix to a ';' separated string
def normalize_multiline_fields(sectors):
    if not sectors or not isinstance(sectors, str):
        return None

    parts = sectors.split('\n- ')

    parts[0] = parts[0].lstrip('- ').strip()

    return ';'.join(part.strip() for part in parts if part.strip())


# Normalize phone numbers to E.164 format
def normalize_phone(phone_str, default_region='US'):
    try:
        parsed = phonenumbers.parse(phone_str, default_region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None
    return None


# Extract email using regex
def extract_email(text):
    email_regex = r'[\w\.-]+@[\w\.-]+\.\w+'
    match = re.search(email_regex, text)
    return match.group(0) if match else None


# Extract phone number using regex and normalize
def extract_phone(text):
    phone_regex = r'(\+?\d{1,2}\s*)?(\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})'
    match = re.search(phone_regex, text)
    if match:
        return normalize_phone(match.group(0))
    return None


def parse_contact_block(raw_contact):
    if not raw_contact or not isinstance(raw_contact, str):
        return None, None, None, None

    # Split by lines and clean up
    lines = [line.strip() for line in raw_contact.split('\n') if line.strip()]

    name = None
    title = None
    phone = None
    email = None

    # Check if the first line contains a comma
    if lines:
        first_line = lines[0]
        if ',' in first_line:
            segments = [s.strip() for s in first_line.split(',')]
            # if more than 2 segments, assume last is title and rest is name
            if len(segments) >= 2:
                title = segments[-1]
                name = ', '.join(segments[:-1])
            else:
                name = segments[0]
        else:
            name = first_line
    # Extract email and phone from the remaining lines
    for line in lines[1:]:
        if not email:
            email = extract_email(line)
        if not phone:
            phone = extract_phone(line)
        if not email and not phone and not title:
            title = line

    return  name, title, email, phone
