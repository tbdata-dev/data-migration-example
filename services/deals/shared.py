from sqlalchemy.orm import Session

from models.deals import Deal


def create_deal(db: Session, deal_data: dict):
    deal = Deal(**deal_data)
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal
