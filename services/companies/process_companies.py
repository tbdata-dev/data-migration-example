from services.companies.pe_comps import map_pe_comps_row
from services.companies.pipelines import map_pipeline_row, map_pipeline_row_bank
from services.companies.shared import create_company, check_company_exists, update_company
from sqlalchemy.orm import Session
from utils.file import read_excel_to_dict
from utils.logger import logger

def process_companies_from_pe_comp(db: Session, filepath: str):

    records = read_excel_to_dict(filepath, sheetname=0, header_row=2, drop_empty=True)
    processed_companies = []

    for row in records:
        try:
            company_data = map_pe_comps_row(row)
            logger.info(f'Row normalized to: {company_data}')

            company = create_company(db, company_data)

            processed_companies.append(company)

        except Exception as e:
            logger.error(f"Error processing row {row} in {filepath}: {e}")
            continue

    return processed_companies


def process_companies_from_pipeline(db: Session, filepath: str, ):

    if filepath == 'data/original_files/Consumer Retail and Healthcare Pipeline.xlsx':
        header_row = 8
    else:
        header_row = 5
    records = read_excel_to_dict(filepath, sheetname=0, header_row=header_row, drop_empty=True)
    processed_companies = []

    for row in records:
        try:
            company_data = map_pipeline_row(row)
            bank_data = map_pipeline_row_bank(row)

            if bank_data:
                for bank in bank_data:
                    bank['name'] = bank['name'].strip()
                    if not bank['name']:
                        logger.warning(f"Row {row} in {filepath} has no bank name. Skipping...")
                        continue
                    existing_company = check_company_exists(db, bank['name'])
                    if existing_company:
                        logger.info(f"Bank {bank['name']} already exists. Updating...")
                        # updated_company = update_company(db, existing_company.id, bank)
                        processed_companies.append(existing_company)
                    else:
                        new_bank = create_company(db, bank)
                        processed_companies.append(new_bank)

            logger.info(f'Row normalized to: {company_data}')

            if not company_data['name']:
                logger.warning(f"Row {row} in {filepath} has no company name. Skipping...")
                continue

            if company_data['name'].lower() in ['Direct to Company', 'Direct to FIS', 'Take-private']:
                logger.warning(f"Row {row} in {filepath} has a placeholder company name. Skipping...")
                continue

            existing_company = check_company_exists(db, company_data['name'])

            if existing_company:
                logger.info(f"Company {company_data['name']} already exists. Updating...")

                # updated_company = update_company(db, existing_company.id, company_data)

                # processed_companies.append(updated_company)
            else:
                new_company = create_company(db, company_data)
                processed_companies.append(new_company)
        except Exception as e:
            logger.error(f"Error processing row {row} in {filepath}: {e}")
            continue

    return processed_companies