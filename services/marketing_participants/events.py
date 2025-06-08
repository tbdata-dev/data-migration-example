from services.contacts.shared import create_contact, check_contact_exists, update_contact
from utils.logger import logger



# process marketing participants from event file
def map_mp_row(db, row, event_name):
    if not row or not isinstance(row, dict):
        logger.error("Invalid row data. Expected a dictionary.")
        return None

    logger.info(f"Mapping marketing participant row: {row}")

    contact_email = row.get('E-mail')
    contact_name = row.get('Name')

    contact = check_contact_exists(db, contact_email, contact_name)

    return {
        'contact_id': contact.id if contact else None,
        'event_name': event_name,
        'status': row.get('Attendee Status').strip() if row.get('Attendee Status') else None,
    }



