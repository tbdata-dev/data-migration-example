from services.contacts.contacts import map_contact_row_from_contacts
from services.contacts.events import map_contact_row_from_events
from services.contacts.pe_comps import map_contact_row_from_pe_comps
from services.contacts.pipelines import map_contact_row_from_pipeline
from utils.file import read_excel_to_dict
from utils.logger import logger
from services.companies.shared import create_company, check_company_exists, update_company
from services.contacts.shared import create_contact, check_contact_exists, update_contact


def process_contacts_from_contacts(db, filepath: str):

    sheets = ["Tier 1's", "Tier 2's"]

    logger.info(f"Processing contacts from {filepath} with sheets: {sheets}")

    processed_contacts = []

    for sheet in sheets:
        records = read_excel_to_dict(filepath, sheetname=sheet, header_row=0, drop_empty=True)

        # Determine tier level based on sheet name
        tier_level = 1 if sheet == "Tier 1's" else 2

        for row in records:
            try:
                contact_data = map_contact_row_from_contacts(row, tier_level)
                logger.info(f'Row normalized to: {contact_data}')

                # Check if company exists
                if contact_data['company']:
                    existing_company = check_company_exists(db, contact_data['company'])
                    if existing_company:
                        contact_data['company_id'] = existing_company.id
                    else:
                        # Create new company if it doesn't exist
                        new_company = create_company(db, {'name': contact_data['company']})
                        contact_data['company_id'] = new_company.id

                existing_contact = check_contact_exists(db, contact_data['email'])
                if existing_contact:
                    logger.info(f"Contact {contact_data['email']} already exists. Updating...")
                    #TODO - identify proper business logic for updating contacts
                    # updated_contact = update_contact(db, existing_contact.id, contact_data)
                    processed_contacts.append(existing_contact)
                else:
                    new_contact = create_contact(db, contact_data)
                    processed_contacts.append(new_contact)

            except Exception as e:
                logger.error(f"Error processing row {row} in {filepath}: {e}")
                continue

    return processed_contacts


def process_contacts_from_events(db, filepath: str):
    sheets = ["Leaders and Partners Dinner", "2019 Market Re-Cap"]

    logger.info(f"Processing contacts from {filepath} with sheets: {sheets}")

    for sheet in sheets:

        records = read_excel_to_dict(filepath, sheetname=sheet, header_row=0, drop_empty=True)
        processed_contacts = []

        for row in records:
            try:
                contact_data = map_contact_row_from_events(row)
                logger.info(f'Row normalized to: {contact_data}')

                existing_contact = check_contact_exists(db, contact_data['email'])
                if existing_contact:
                    logger.info(f"Contact {contact_data['email']} already exists. Updating...")
                    #TODO - identify proper business logic for updating contacts
                    # updated_contact = update_contact(db, existing_contact.id, contact_data)
                    processed_contacts.append(existing_contact)
                else:
                    new_contact = create_contact(db, contact_data)
                    processed_contacts.append(new_contact)

            except Exception as e:
                logger.error(f"Error processing row {row} in {filepath}: {e}")
                continue

        return processed_contacts


def process_contacts_from_pe_comps(db, filepath: str):
    records = read_excel_to_dict(filepath, sheetname=0, header_row=2, drop_empty=True)
    processed_contacts = []

    for row in records:
        try:
            contact_data_list = map_contact_row_from_pe_comps(row)

            for contact_data in contact_data_list:

                logger.info(f'Row normalized to: {contact_data}')

                # Check if company exists
                if contact_data['company']:
                    existing_company = check_company_exists(db, contact_data['company'])
                    if existing_company:
                        contact_data['company_id'] = existing_company.id
                    else:
                        # Create new company if it doesn't exist
                        new_company = create_company(db, {'name': contact_data['company']})
                        contact_data['company_id'] = new_company.id

                existing_contact = check_contact_exists(db, contact_data['email'])
                if existing_contact:
                    logger.info(f"Contact {contact_data['email']} already exists. Updating...")
                    #TODO - identify proper business logic for updating contacts
                    #updated_contact = update_contact(db, existing_contact.id, contact_data)
                    processed_contacts.append(existing_contact)
                else:
                    new_contact = create_contact(db, contact_data)
                    processed_contacts.append(new_contact)

        except Exception as e:
            logger.error(f"Error processing row {row} in {filepath}: {e}")
            continue

    return processed_contacts


def process_contacts_from_pipeline(db, filepath: str):
    if filepath == 'data/original_files/Consumer Retail and Healthcare Pipeline.xlsx':
        header_row = 8
    else:
        header_row = 5

    records = read_excel_to_dict(filepath, sheetname=0, header_row=header_row, drop_empty=True)
    processed_contacts = []

    for row in records:
        try:
            contact_rows = map_contact_row_from_pipeline(row)

            for contact_data in contact_rows:
                if not contact_data:
                    continue

                logger.info(f'Row normalized to: {contact_data}')

                # Check if company exists
                if contact_data['company']:
                    existing_company = check_company_exists(db, contact_data['company'])
                    if existing_company:
                        contact_data['company_id'] = existing_company.id
                    else:
                        # Create new company if it doesn't exist
                        new_company = create_company(db, {'name': contact_data['company']})
                        contact_data['company_id'] = new_company.id

                existing_contact = check_contact_exists(db, contact_data['email'], contact_data['name'], contact_data['company'])
                if existing_contact:
                    logger.info(f"Contact {contact_data['email']} already exists. Updating...")
                    #TODO - identify proper business logic for updating contacts
                    # updated_contact = update_contact(db, existing_contact.id, contact_data)
                    processed_contacts.append(existing_contact)
                else:
                    new_contact = create_contact(db, contact_data)
                    processed_contacts.append(new_contact)

        except Exception as e:
            logger.error(f"Error processing row {row} in {filepath}: {e}")
            continue

    return processed_contacts
