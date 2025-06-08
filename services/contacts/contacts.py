from utils.logger import logger
from datetime import datetime
from utils.data import normalize_phone_number


def map_contact_row_from_contacts(row, tier_level):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping contact row: {row}")

    city, state, country = parse_city_state_country(row.get('City'))
    logger.info(f"Parsed city: {city}, state: {state}, country: {country}")
    return {
        'name': row.get('Name'),
        'company': row.get('Firm'),
        'title': normalize_titles(row.get('Title')),
        'group': row.get('Group'),
        'sub_vertical': row.get('Sub-Vertical'),
        'email': row.get('E-mail').lower() if row.get('E-mail') else None,
        'phone': normalize_phone_number(row.get('Phone')),
        'secondary_phone': normalize_phone_number(row.get('Secondary Phone')),
        'city': city,
        'state': state,
        'country': country,
        'birthday': normalize_birthday(row.get('Birthday')),
        'coverage_person': row.get('Coverage Person'),
        'preferred_contact_method': row.get('Preferred Contact Method'),
        'tier': tier_level,
    }


# split city, state, and country from the city field in the sheet
def parse_city_state_country(city):

    logger.info(f"Parsing city, state, country from: {city}")
    if not city or not isinstance(city, str):
        return None, None, None

    parts = city.split(',')

    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip(), 'US'
    elif len(parts) == 1:
        return None, None, parts[0].strip()
    else:
        return None, None, None


# Change titles to a ';' separated string to match the format in the database
def normalize_titles(title):
    if not title or not isinstance(title, str):
        return None
    parts = title.split(',')

    return '; '.join(part.strip() for part in parts if part.strip()) if parts else None


# Parse date from birthday string in the format 'MM/DD/YYYY'
def normalize_birthday(birthday):
    if not birthday or not isinstance(birthday, str):
        return None
    try:
        return datetime.strptime(birthday, '%m/%d/%Y').date()
    except ValueError:
        logger.error(f'Invalid birthday format: {birthday}')
        return None

