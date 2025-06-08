from sqlalchemy.orm import Session
from models.contacts import Contact
from models.companies import Company
from sqlalchemy import func


def create_contact(db: Session, contact_data: dict):
    if 'company' in contact_data:
        contact_data.pop('company')

    contact = Contact(**contact_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def check_contact_exists(db: Session, email: str = None, name: str = None, company_name: str = None):
    # First try matching on email
    if email:
        contact = db.query(Contact).filter(func.lower(Contact.email) == email.strip().lower()).first()
        if contact:
            return contact

    # Fallback: try matching on name + company
    if name and company_name:
        company = (
            db.query(Company)
            .filter(func.lower(Company.name) == company_name.strip().lower())
            .first()
        )
        if company:
            contact = (
                db.query(Contact)
                .filter(Contact.name == name, Contact.company_id == company.id)
                .first()
            )
            return contact

    return None


def update_contact(db: Session, contact_id: int, contact_data: dict):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise ValueError(f"Contact with id {contact_id} does not exist.")

    for key, value in contact_data.items():
        if value is not None:
            setattr(contact, key, value)

    db.commit()
    db.refresh()

    return contact
