from services.companies.process_companies import process_companies_from_pe_comp, process_companies_from_pipeline
from services.contacts.process_contacts import (process_contacts_from_contacts, process_contacts_from_events,
                                                process_contacts_from_pe_comps, process_contacts_from_pipeline)
from services.deals.process_deals import process_deals_from_pipeline
from services.marketing_participants.process_marketing_participants import process_mps_from_events
from services.export_data_to_csv import export_all_tables_to_csv
from models.base import init_db, SessionLocal, engine
from utils.logger import logger



if __name__ == "__main__":
    init_db()
    logger.info("Database initialized")

    db = SessionLocal()
    logger.info("Database session created")

    try:
        logger.info("Starting data processing...")

        # create companies from PE Comps and Pipeline files

        logger.info("Processing companies...")
        process_companies_from_pe_comp(db, "data/original_files/PE Comps.xlsx")
        process_companies_from_pipeline(db, "data/original_files/Consumer Retail and Healthcare Pipeline.xlsx")
        process_companies_from_pipeline(db, "data/original_files/Business Services Pipeline.xlsx")

        # create contacts

        logger.info("Processing contacts...")
        process_contacts_from_contacts(db, "data/original_files/Contacts.xlsx")
        process_contacts_from_events(db, "data/original_files/Events.xlsx")
        process_contacts_from_pe_comps(db, "data/original_files/PE Comps.xlsx")
        process_contacts_from_pipeline(db, "data/original_files/Consumer Retail and Healthcare Pipeline.xlsx")

        # create deals

        logger.info("Processing deals...")
        process_deals_from_pipeline(db, "data/original_files/Consumer Retail and Healthcare Pipeline.xlsx")
        process_deals_from_pipeline(db, "data/original_files/Business Services Pipeline.xlsx")

        # create marketing participants

        logger.info("Processing marketing participants...")
        process_mps_from_events(db, "data/original_files/Events.xlsx")

        logger.info("Data processing completed.")
    except Exception as e:
        logger.error(f"Error processing file: {e}")

    finally:
        export_all_tables_to_csv(engine)
        db.close()
        logger.info("Database session closed.")