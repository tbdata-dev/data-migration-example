from sqlalchemy.orm import Session
from models.companies import Company
from sqlalchemy import func


def create_company(db: Session, company_data: dict):

    company = Company(**company_data)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def check_company_exists(db: Session, company_name: str):
    if not company_name:
        return None

    company_name = company_name.strip().lower()

    company = (
        db.query(Company)
        .filter(func.lower(Company.name) == company_name)
        .first()
    )
    return company if company else None


def update_company(db: Session, company_id: int, company_data: dict):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise ValueError(f"Company with id {company_id} does not exist.")

    for key, value in company_data.items():
        if value is not None:
            setattr(company, key, value)

    db.commit()
    db.refresh()

    return company
